import pandas as pd
import mysql.connector

# Connect to local MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@statisticsS1",  # your MySQL password
    database="dental_ai_mvp"
)

# Fetch appointments
df = pd.read_sql("SELECT * FROM appointments ORDER BY date_time ASC", conn)
conn.close()

# Save to CSV for Streamlit Cloud
df.to_csv("sample_appointments.csv", index=False)
print("✅ sample_appointments.csv created successfully!")