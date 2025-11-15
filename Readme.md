# InvolyticsN

InvolyticsN is an AI agentic workflow designed to extract structured information from invoice images, store the extracted data efficiently, and enable intelligent querying and analysis.  
The system leverages Vision-Language Models (VLMs), multi-agent orchestration, and modern data engineering tools to build a complete invoice analytics pipeline.

---

## ✨ Key Features

- 📄 Invoice Image Understanding using the Hugging Face model  
  **`Qwen/Qwen2.5-VL-7B-Instruct`**
- 🧠 Agentic Pipeline using **Agno Agents**
- 🗄️ Raw Data Capture in **MongoDB**
- 🏛️ Processed Data Storage in **Postgres**
- ⛓️ Workflow Automation with **Apache Airflow**
- 🎛️ Observability integrated via **Langfuse**
- 📊 Dual-Agent Query System:
  1. Invoice-specific Q&A (MongoDB)
  2. Analytical/Trend Q&A (Postgres)

---

## 🏗️ Architecture Overview
https://code2tutorial.com/tutorial/afb506e0-ded4-4d27-b73d-2a66353bde9e/index.md


---

## 🧩 Agents

| Agent | Purpose | Data Source |
|------|---------|-------------|
| **Invoice Agent** | Processes invoice images and answers questions related to a specific **bill number** | **MongoDB** |
| **Analytics Agent** | Handles **summary / aggregated / trend** questions | **PostgresDB** |

Agents and Tool definitions located in:

A Pydantic model is used to enforce structured extraction from the VLM.

---

## 🧱 Data Flow

1. Invoice images are uploaded.
2. VLM extracts raw structured fields using a Pydantic schema.
3. Raw extracted data is stored in **MongoDB**.
4. **Apache Airflow** transforms and loads the processed data into **Postgres**.
5. Agents query their respective databases based on the question type.

---

## ⚙️ Tech Stack

| Component | Technology |
|----------|------------|
| Model | `Qwen/Qwen2.5-VL-7B-Instruct` |
| Agent Framework | Agno Agents |
| Observability | Langfuse |
| ETL & Workflow | Apache Airflow |
| Raw Data Store | MongoDB |
| Processed Data Store | PostgresDB |
| Schema Validation | Pydantic Models |

---

## 🚀 Future Enhancements

- Enhanced template generalization across invoice layouts
- UI dashboard for analytics and exploration
- Add RAG-based invoice retrieval and semantic search
- Faster inference

---

## 🤝 Contributing

Contributions are welcome!  
Please open issues or submit pull requests to improve this project.

---

## 📜 License

This project is licensed under the **MIT License**.




