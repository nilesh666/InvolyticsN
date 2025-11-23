from airflow.decorators import task
from airflow import DAG
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pendulum import datetime
import re
import json

with DAG(
    dag_id = "agno_mongo_test",
    # start_date = datetime(2025, 11,15),
    schedule='@daily'
) as dag:
    
    @task
    def create_table_postgres():
        postgres_hook = PostgresHook(postgres_conn_id = "postgres_default" )
        create_table_query = """
        CREATE TABLE IF NOT EXISTS sales_data(
            file_name TEXT,
            invoice_number TEXT PRIMARY KEY,
            seller_name TEXT,
            client_name TEXT,
            date_of_issue DATE,
            vat_percentage NUMERIC(5,2),
            net_worth NUMERIC(12,2),
            vat NUMERIC(12,2),
            gross_worth NUMERIC(12,2)
        );
        """

        postgres_hook.run(create_table_query)

        # invoice_numbers = []
        # get_invoice_number_query = """
        # select invoice_number from sales_data
        # """
        # records=postgres_hook.get_records(get_invoice_number_query)
        # invoice_numbers=[r[0] for r in records]
        # return invoice_numbers
        return "Done"

    @task
    def get_mongo_contents():
        mongo_hook = MongoHook(mongo_conn_id="mongo_default")
        collection = mongo_hook.get_collection("processed")
        docs = collection.find({}, {"_id": 0})
        dl=[]
        for doc in docs:
            data={}
            file_name = doc.get("file_name")
            vlm_response = doc.get("vlm_response", "")
            match = re.search(r'\{.*\}', vlm_response, re.DOTALL)
            if not match:
                print("No data")
                continue

            resp = json.loads(match.group(0))
            data = {
                "file_name": file_name,
                "invoice_number": resp.get("invoice", {}).get("number"),
                "seller_name": resp.get("seller", {}).get("name"),
                "client_name": resp.get("client", {}).get("name"),
                "date_of_issue": resp.get("invoice", {}).get("date"),
                "vat_percentage": resp.get("summary", {}).get("vat_percentage"),
                "net_worth": resp.get("summary", {}).get("net_worth"),
                "vat": resp.get("summary", {}).get("vat"),
                "gross_worth": resp.get("summary", {}).get("gross_worth"),  
            }
            dl.append(data)
        return dl
            
    @task
    def load_to_postgres(data_list):
        columns = ["file_name", "invoice_number", "seller_name", "client_name", "date_of_issue", "vat_percentage", "net_worth", "vat", "gross_worth"]
        rows = [
            tuple(d[col] for col in  columns)
            for d in data_list
        ]
        postgres_hook = PostgresHook(postgres_conn_id = "postgres_default" )
        postgres_hook.insert_rows(
            table="sales_data",
            rows=rows,
            target_fields=columns,
            commit_every=50
        )        

    @task
    def delete_duplicates_postgres():
        postgres_hook = PostgresHook(postgres_conn_id = "postgres_default" )
        delete_duplicate_query = """
            DELETE FROM sales_data
            WHERE ctid NOT IN (
            SELECT MAX(ctid)
            FROM sales_data
            GROUP BY file_name, invoice_number, seller_name, client_name,
                     date_of_issue, vat_percentage, net_worth, vat, gross_worth
            );
        """
        postgres_hook.run(delete_duplicate_query)

    create = create_table_postgres()
    mongo_data = get_mongo_contents()
    load = load_to_postgres(mongo_data)
    delete = delete_duplicates_postgres()

    create >> mongo_data >> load >> delete

