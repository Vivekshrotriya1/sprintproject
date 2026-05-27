import pandas as pd

from sklearn.model_selection import (
    train_test_split
)

# LOAD DATASET

df = pd.read_csv(
    "../data/processed/cleaned_walmart_dataset.csv"
)

print("Dataset Loaded Successfully!")

# FEATURES & TARGET

X = df.drop(
    'Weekly_Sales',
    axis=1
)

y = df['Weekly_Sales']

print("Features & Target Created!")

# TRAIN TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42
)

print("Train-Test Split Completed!")

print("X_train Shape:", X_train.shape)

print("X_test Shape:", X_test.shape)