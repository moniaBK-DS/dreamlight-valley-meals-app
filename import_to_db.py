import pandas as pd
import sqlite3

# Load your corrected CSV
df = pd.read_csv("Recipes-Table-1.csv")

# Drop unnamed columns and clean headers
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df.columns = df.columns.str.strip().str.replace('"', '').str.replace(' ', '_').str.lower()

# Create SQLite DB and write the table
conn = sqlite3.connect("dreamlight_meals.db")
df.to_sql("meals", conn, if_exists="replace", index=False)
conn.close()

print("✅ Database created with meals table.")
