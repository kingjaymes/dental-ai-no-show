import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime

# ----------------------------
# Connect to MySQL
# ----------------------------
def get_appointments():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@statisticsS1",  # replace with your MySQL password
        database="dental_ai_mvp"
    )
    df = pd.read_sql("SELECT * FROM appointments ORDER BY date_time ASC", conn)
    conn.close()
    return df

# ----------------------------
# Streamlit Dashboard
# ----------------------------
st.set_page_config(page_title="Dental AI Dashboard", layout="wide")
st.title("🦷 Dental AI - No-Show Risk Dashboard")

# Load data
df = get_appointments()

# Sidebar filters
st.sidebar.header("Filters")
risk_filter = st.sidebar.multiselect("Select Risk Level", options=df['risk_level'].unique(), default=df['risk_level'].unique())
day_filter = st.sidebar.multiselect("Select Day of Week", options=df['date_time'].dt.day_name().unique(), default=df['date_time'].dt.day_name().unique())

# Filter dataframe
df['day_name'] = df['date_time'].dt.day_name()
filtered_df = df[(df['risk_level'].isin(risk_filter)) & (df['day_name'].isin(day_filter))]

# Show filtered appointments
st.subheader(f"Upcoming Appointments ({len(filtered_df)})")
st.dataframe(filtered_df[['appointment_id','patient_id','date_time','risk_score','risk_level','appointment_type']])

# Highlight high-risk appointments
st.subheader("High-Risk Appointments")
high_risk_df = filtered_df[filtered_df['risk_level']=='High']
st.dataframe(high_risk_df[['appointment_id','patient_id','date_time','risk_score','appointment_type']])