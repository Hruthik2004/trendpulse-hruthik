# Import required libraries
import pandas as pd
import json
import os

# Step 1: Load JSON file

# Get latest JSON file from data folder
folder = "data"
files = [f for f in os.listdir(folder) if f.endswith(".json")]

# Sort and pick latest file
latest_file = sorted(files)[-1]
file_path = os.path.join(folder, latest_file)

# Load JSON data
with open(file_path, "r") as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

print(f"Loaded {len(df)} stories from {file_path}")


# Step 2: Data Cleaning

# 1. Remove duplicates based on post_id
before = len(df)
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# 2. Remove rows with missing values
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# 3. Fix data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# 4. Remove low quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# 5. Remove extra whitespace from titles
df["title"] = df["title"].str.strip()


# Step 3: Save cleaned data to CSV

output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")


# Step 4: Print summary (stories per category)

print("\nStories per category:")
print(df["category"].value_counts())