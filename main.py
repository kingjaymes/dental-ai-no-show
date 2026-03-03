from fastapi import FastAPI, UploadFile, File
import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import datetime


app = FastAPI(title="Dental Clinic AI MVP")

# -------------------
# MySQL Connection
# -------------------
def get_connection():
    connection = mysql.connector.connect(
        host="localhost",      # Replace with your MySQL host
        user="root",           # Replace with your MySQL user
        password="@statisticsS1",   # Replace with your MySQL password
        database="dental_ai_mvp"
    )
    return connection

# -------------------
# Endpoint: Upload Appointments CSV
# -------------------
@app.post("/upload-appointments")
async def upload_appointments(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        connection = get_connection()
        cursor = connection.cursor()
        for _, row in df.iterrows():
            sql = """
            INSERT INTO appointments 
            (patient_id, date_time, appointment_type, past_attendance, booking_lead_time) 
            VALUES (%s,%s,%s,%s,%s)
            """
            cursor.execute(sql, (
                int(row['patient_id']),
                row['date_time'],
                row['appointment_type'],
                int(row['past_attendance']),
                int(row['booking_lead_time'])
            ))
        connection.commit()
        cursor.close()
        connection.close()
        return {"status": "success", "message": f"{len(df)} appointments uploaded"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# -------------------
# Endpoint: Get Appointments
# -------------------
@app.get("/appointments")
def get_appointments():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM appointments ORDER BY date_time ASC LIMIT 100")
        appointments = cursor.fetchall()
        cursor.close()
        connection.close()
        return appointments
    except Exception as e:
        return {"status": "error", "message": str(e)}

# -------------------
# Endpoint: Send Reminder (Mock)
# -------------------
@app.post("/send-reminder/{appointment_id}")
def send_reminder(appointment_id: int, channel: str = "SMS"):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sent_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            INSERT INTO reminders (appointment_id, sent_at, channel, status)
            VALUES (%s,%s,%s,%s)
        """, (appointment_id, sent_at, channel, "Sent"))
        connection.commit()
        cursor.close()
        connection.close()
        return {"status": "success", "message": f"Reminder sent for appointment {appointment_id}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# -------------------
# Endpoint: Update Risk Score (Mock)
# -------------------
@app.post("/update-risk/{appointment_id}")
def update_risk(appointment_id: int, risk_score: float, risk_level: str):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE appointments 
            SET risk_score=%s, risk_level=%s 
            WHERE appointment_id=%s
        """, (risk_score, risk_level, appointment_id))
        connection.commit()
        cursor.close()
        connection.close()
        return {"status": "success", "message": f"Risk updated for appointment {appointment_id}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
# main.py

# ----------------------------
# Imports
# ----------------------------
from fastapi import FastAPI, HTTPException
import pandas as pd
import joblib

# ----------------------------
# FastAPI app
# ----------------------------
app = FastAPI(title="Dental AI No-Show Prediction API")

# ----------------------------
# Load trained model (Step 1)
# ----------------------------
try:
    model = joblib.load("no_show_model.pkl")
    print("✅ No-show prediction model loaded successfully.")
except Exception as e:
    print("❌ Error loading model:", e)

# ----------------------------
# Predict risk endpoint (Step 2)
# ----------------------------
@app.post("/predict-risk/")
async def predict_risk(appointment: dict):
    """
    Predict risk_score and risk_level for a single appointment.
    Expected JSON fields:
    - past_attendance: int
    - booking_lead_time: int
    - day_of_week: int (0=Monday, 6=Sunday)
    - appointment_type_Consultation, appointment_type_Extraction, appointment_type_Whitening: 0/1
    """
    try:
        df_input = pd.DataFrame([appointment])
        risk_prob = model.predict_proba(df_input)[:, 1][0]

        if risk_prob < 0.4:
            risk_level = "Low"
        elif risk_prob < 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"

        return {
            "risk_score": round(risk_prob, 2),
            "risk_level": risk_level
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

import mysql.connector
from datetime import datetime

def update_upcoming_risks():
    # Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@statisticsS1",  # your MySQL password
        database="dental_ai_mvp"
    )
    cursor = conn.cursor(dictionary=True)

    # Fetch upcoming appointments
    cursor.execute("SELECT * FROM appointments WHERE date_time >= NOW()")
    appointments = cursor.fetchall()

    for appt in appointments:
        # Prepare features
        features = {
            "past_attendance": appt["past_attendance"],
            "booking_lead_time": appt["booking_lead_time"],
            "day_of_week": appt["date_time"].weekday(),
            "appointment_type_Consultation": 1 if appt.get("appointment_type_Consultation",0) else 0,
            "appointment_type_Extraction": 1 if appt.get("appointment_type_Extraction",0) else 0,
            "appointment_type_Whitening": 1 if appt.get("appointment_type_Whitening",0) else 0
        }

        # Predict risk
        df_input = pd.DataFrame([features])
        risk_prob = model.predict_proba(df_input)[:,1][0]

        if risk_prob < 0.4:
            risk_level = "Low"
        elif risk_prob < 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"

        # Update DB
        cursor.execute(
            "UPDATE appointments SET risk_score=%s, risk_level=%s WHERE appointment_id=%s",
            (round(risk_prob,2), risk_level, appt["appointment_id"])
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Upcoming appointments updated with AI risk scores.")

if __name__ == "__main__":
    update_upcoming_risks()