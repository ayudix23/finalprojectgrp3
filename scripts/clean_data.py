import pandas as pd

# Load dataset
df = pd.read_csv("datasets/twitter/amazon_clean_data.csv")

# Show available columns
print("Columns:")
print(df.columns.tolist())

# Remove duplicate rows
df = df.drop_duplicates()

# Remove completely empty rows
df = df.dropna(how="all")

# Convert all string columns to lowercase
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].astype(str).str.lower()

# Save cleaned file
df.to_csv(
    "datasets/processed/amazon_clean.csv",
    index=False
)

print("Cleaning complete")
print("Shape:", df.shape)