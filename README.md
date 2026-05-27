# Walmart AI Retail Project
walmart-ai-retail-project/
│
├── data/
│   ├── raw/
│   │   ├── train.csv
│   │   ├── features.csv
│   │   ├── stores.csv
│   │
│   ├── processed/
│   │   ├── cleaned_walmart_dataset.csv
│
├── models/
│   ├── walmart_pipeline_model.pkl
│
├── src/
│   │
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   ├── preprocessing_pipeline.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── save_model.py
│   ├── predict.py
│
├── api/
│   ├── app.py
│   ├── routes/
│   │   ├── prediction.py
│   │   ├── analytics.py
│   │   ├── anomaly.py
│
├── agents/
│   ├── sales_agent.py
│   ├── analytics_agent.py
│   ├── chatbot_agent.py
│
├── dashboard/
│   ├── walmart_dashboard.pbix
│
├── deployment/
│   ├── Dockerfile
│   ├── requirements.txt
│
└── README.md