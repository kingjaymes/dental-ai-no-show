import pandas as pd
import mysql.connector

def export_appointments_to_csv():
    # Connect to your local MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@statisticsS1",  # your MySQL password
        database="dental_ai_mvp"
    )

    # Fetch all appointments
    df = pd.read_sql("SELECT * FROM appointments ORDER BY date_time ASC", conn)
    conn.close()

    # Save to CSV
    df.to_csv("sample_appointments.csv", index=False)
    print("✅ sample_appointments.csv updated successfully!")

if __name__ == "__main__":
    export_appointments_to_csv()