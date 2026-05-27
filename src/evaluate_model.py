import pandas as pd
import pickle

from sklearn.model_selection import (
    train_test_split
)

from sklearn.metrics import (
    r2_score,
    mean_absolute_error
)


df = pd.read_csv(
    "../data/processed/cleaned_walmart_dataset.csv"
)

# FEATURES & TARGET

X = df.drop(
    'Weekly_Sales',
    axis=1
)

y = df['Weekly_Sales']

# TRAIN TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42
)

# LOAD MODEL

model = pickle.load(

    open(
        "../models/walmart_pipeline_model.pkl",
        'rb'
    )
)

# PREDICTIONS

train_preds = model.predict(
    X_train
)

test_preds = model.predict(
    X_test
)

# METRICS

train_r2 = r2_score(
    y_train,
    train_preds
)

test_r2 = r2_score(
    y_test,
    test_preds
)

train_mae = mean_absolute_error(
    y_train,
    train_preds
)

test_mae = mean_absolute_error(
    y_test,
    test_preds
)

# REPORT


print(" WALMART SALES FORECASTING MODEL REPORT")


print(
    f" TRAIN DATA Accuracy : {train_r2 * 100:.2f}%"
)

print(
    f" TEST DATA Accuracy  : {test_r2 * 100:.2f}%"
)

print(
    f" Train MAE : {train_mae:.2f}"
)

print(
    f" Test MAE  : {test_mae:.2f}"
)
