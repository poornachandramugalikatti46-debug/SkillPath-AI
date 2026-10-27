import pandas as pd

# Load dataset
df = pd.read_csv("data/student_training_data.csv")

print("=" * 50)
print("SKILLPATH AI DATASET EXPLORATION")
print("=" * 50)


# Shape
print("\n1. Dataset Shape:")
print(df.shape)


# Columns
print("\n2. Columns:")
print(df.columns.tolist())


# First 5 rows
print("\n3. First 5 Rows:")
print(df.head())


# Data types
print("\n4. Data Types:")
print(df.dtypes)


# Missing values
print("\n5. Missing Values:")
print(df.isnull().sum())


# Duplicate rows
print("\n6. Duplicate Rows:")
print(df.duplicated().sum())


# Statistics
print("\n7. Statistical Summary:")
print(df.describe())


# Readiness distribution
print("\n8. Readiness Categories:")
print(df["readiness_category"].value_counts())


# Readiness score statistics
print("\n9. Readiness Score:")
print(df["readiness_score"].describe())