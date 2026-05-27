


import pandas as pd

# LOAD DATASET

df = pd.read_csv(
    "../data/raw/merged_walmart_dataset.csv"
)

print("Dataset Loaded Successfully!")

# HANDLE MISSING VALUES

markdown_cols = [
    'MarkDown1',
    'MarkDown2',
    'MarkDown3',
    'MarkDown4',
    'MarkDown5'
]

for col in markdown_cols:
    df[col] = df[col].fillna(df[col].mean())

print("Missing values handled successfully!")

# REMOVE DUPLICATES

df.drop_duplicates(inplace=True)

print("Duplicates removed successfully!")

df.to_csv(
    "../data/processed/cleaned_walmart_dataset.csv",
    index=False
)