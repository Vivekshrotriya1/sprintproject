import pandas as pd

from sklearn.model_selection import (
    train_test_split
)

from sklearn.pipeline import Pipeline

from xgboost import XGBRegressor

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(
    "../data/processed/cleaned_walmart_dataset.csv"
)

print("Dataset Loaded Successfully!")

# ==========================================
# FEATURES & TARGET
# ==========================================

X = df.drop(
    'Weekly_Sales',
    axis=1
)

y = df['Weekly_Sales']

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42
)

# ==========================================
# CREATE PIPELINE
# ==========================================

pipeline = Pipeline(

    steps=[

        (

            'model',

            XGBRegressor(

                n_estimators=100,

                learning_rate=0.1,

                max_depth=6,

                random_state=42
            )
        )
    ]
)

print("Pipeline Created Successfully!")

# ==========================================
# TRAIN MODEL
# ==========================================

pipeline.fit(
    X_train,
    y_train
)

print("Pipeline Trained Successfully!")