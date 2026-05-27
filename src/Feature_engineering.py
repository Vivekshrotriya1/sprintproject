import pandas as pd

# LOAD CLEANED DATASET

df = pd.read_csv(
    "../data/processed/cleaned_walmart_dataset.csv"
)

# CONVERT DATE COLUMN

df['Date'] = pd.to_datetime(df['Date'])

# CREATE DATE FEATURES

df['Year'] = df['Date'].dt.year

df['Month'] = df['Date'].dt.month

df['Week'] = df['Date'].dt.isocalendar().week

print("Date features created successfully!")

# DROP ORIGINAL DATE COLUMN
df.drop('Date', axis=1, inplace=True)

# CONVERT IsHoliday TO BINARY

df['IsHoliday'] = df['IsHoliday'].astype(int)

print("IsHoliday converted successfully!")

# ONE HOT ENCODING

df = pd.get_dummies(
    df,
    columns=['Type'],
    drop_first=True
)


df['Type_B'] = df['Type_B'].astype(int)

df['Type_C'] = df['Type_C'].astype(int)

print("Type columns converted successfully!")

# SAVE FEATURE ENGINEERED DATASET


df.to_csv(
    "../data/processed/cleaned_walmart_dataset.csv",
    index=False
)

print("Feature engineered dataset saved!")