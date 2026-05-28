# Walmart AI Retail Assistant

This project is a FastAPI-based Walmart retail analytics assistant. It supports sales prediction, data ingestion, anomaly detection, and an agent-chat interface for retail, inventory, and policy-related questions.

## Main Features

- Data ingestion into MongoDB
- Sales prediction using a trained ML model
- Sales anomaly detection using the processed Walmart dataset from Azure Blob Storage
- Agent chat for:
  - Retail strategy queries
  - Inventory optimization queries
  - Policy compliance queries
- Azure Web App deployment using GitHub Actions CI/CD
- Lightweight policy RAG using TF-IDF retrieval over saved policy chunks

## High-Level Architecture

```mermaid
flowchart TD
    User["User / FastAPI Docs"] --> API["FastAPI App"]

    API --> Ingestion["/data-ingestion"]
    API --> Prediction["/predict-sales"]
    API --> Anomaly["/sales-anomalies"]
    API --> Chat["/agent-chat"]

    Ingestion --> MongoDB["MongoDB retail_data"]
    Prediction --> Model["walmart_pipeline_model.pkl"]
    Prediction --> MongoDB

    Anomaly --> Blob["Azure Blob Storage"]
    Blob --> Dataset["cleaned_walmart_dataset.csv"]
    Dataset --> Cache["/tmp cached CSV"]
    Cache --> Anomaly

    Chat --> Router["Agent Router"]
    Router --> Retail["Retail Strategy Agent"]
    Router --> Inventory["Inventory Optimization Agent"]
    Router --> Policy["Policy Compliance Agent"]

    Retail --> PandasAI["PandasAI + Dataset"]
    Inventory --> PandasAI
    Policy --> RAG["TF-IDF Policy RAG"]
    RAG --> Chunks["chunks.pkl"]

    Retail --> AzureOpenAI["Azure OpenAI"]
    Inventory --> AzureOpenAI
    Policy --> AzureOpenAI
```

## API Flow

```mermaid
sequenceDiagram
    participant User
    participant FastAPI
    participant MongoDB
    participant Model

    User->>FastAPI: POST /data-ingestion
    FastAPI->>MongoDB: Insert retail record
    MongoDB-->>FastAPI: inserted_id
    FastAPI-->>User: Data inserted successfully

    User->>FastAPI: GET /predict-sales
    FastAPI->>MongoDB: Fetch latest record
    FastAPI->>Model: Predict sales
    FastAPI->>MongoDB: Save predicted sales
    FastAPI-->>User: Predicted weekly sales
```

## Agent Chat Flow

```mermaid
flowchart TD
    Query["User Query"] --> Keyword["Keyword Router"]

    Keyword -->|Sales / Store / Revenue| Retail["Retail Strategy Agent"]
    Keyword -->|Inventory / Stock / Demand| Inventory["Inventory Optimization Agent"]
    Keyword -->|Policy / HR / Compliance| Policy["Policy Compliance Agent"]
    Keyword -->|No keyword match| AzureRouter["Azure OpenAI Router"]

    AzureRouter --> Retail
    AzureRouter --> Inventory
    AzureRouter --> Policy
    AzureRouter --> Blocked["Blocked Query"]

    Retail --> RetailEngine["PandasAI Retail Analysis"]
    Inventory --> InventoryEngine["PandasAI Inventory Analysis"]
    Policy --> PolicyRAG["Lightweight TF-IDF RAG"]

    RetailEngine --> Response["Formatted Response"]
    InventoryEngine --> Response
    PolicyRAG --> Response
```

## Dataset Flow

The large processed dataset is not stored in GitHub. It is stored in Azure Blob Storage and downloaded at runtime.

```mermaid
flowchart LR
    Blob["Azure Blob Storage Container"] --> CSV["cleaned_walmart_dataset.csv"]
    CSV --> Temp["/tmp/cleaned_walmart_dataset.csv"]
    Temp --> Pandas["Pandas DataFrame"]
    Pandas --> Anomaly["/sales-anomalies"]
    Pandas --> AgentChat["/agent-chat Retail and Inventory"]
```

Required Azure App Settings:

```text
AZURE_STORAGE_CONNECTION_STRING
AZURE_CONTAINER_NAME
RETAIL_DATASET_BLOB=cleaned_walmart_dataset.csv
```

`RETAIL_DATASET_BLOB` is optional if the blob name is exactly:

```text
cleaned_walmart_dataset.csv
```

## Policy RAG Flow

The policy agent uses lightweight RAG. It does not use FAISS, Chroma, vector databases, or sentence-transformer embeddings in deployment.

```mermaid
flowchart TD
    PolicyPDF["policy.pdf"] --> Setup["rag_setup.py"]
    Setup --> Chunks["chunks.pkl"]
    UserQuery["Policy Query"] --> TFIDF["TF-IDF Similarity Search"]
    Chunks --> TFIDF
    TFIDF --> Context["Top Relevant Policy Chunks"]
    Context --> AzureOpenAI["Azure OpenAI"]
    AzureOpenAI --> Answer["Grounded Policy Answer"]
```

Runtime file required:

```text
agents/rag_data/chunks.pkl
```

Helper file for regenerating chunks when the policy PDF changes:

```text
agents/rag_data/rag_setup.py
```

## Azure CI/CD Flow

```mermaid
flowchart TD
    Dev["Developer Push to GitHub"] --> Actions["GitHub Actions"]
    Actions --> Checkout["Checkout Repo + LFS Check"]
    Checkout --> Package["Create Lightweight Deployment Package"]
    Package --> Requirements["Use requirements-azure.txt"]
    Requirements --> Deploy["Deploy to Azure Web App"]
    Deploy --> Startup["bash startup.sh"]
    Startup --> FastAPI["FastAPI Running on Azure"]
```

## Important Azure Startup Command

Use this startup command in Azure Web App:

```bash
bash startup.sh
```

## Important Environment Variables

```text
MONGO_URL
AZURE_OPENAI_API_KEY
AZURE_OPENAI_API_VERSION
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_DEPLOYMENT
AZURE_STORAGE_CONNECTION_STRING
AZURE_CONTAINER_NAME
RETAIL_DATASET_BLOB
SCM_DO_BUILD_DURING_DEPLOYMENT=true
ENABLE_ORYX_BUILD=true
```

## Main Endpoints

```text
POST /data-ingestion
GET  /predict-sales
GET  /sales-anomalies
POST /agent-chat
GET  /all-predictions
GET  /docs
```

## Testing Order

1. Open `/docs`
2. Insert data using `/data-ingestion`
3. Run `/predict-sales`
4. Run `/sales-anomalies`
5. Run `/agent-chat`

## Notes

- The root path `/` may return `404 Not Found`; use `/docs` for FastAPI Swagger UI.
- The processed CSV is loaded from Azure Blob Storage and cached in `/tmp`.
- Policy RAG is TF-IDF based and uses `chunks.pkl`.
- The ML model file must be committed as a real pickle file, not a Git LFS pointer.
