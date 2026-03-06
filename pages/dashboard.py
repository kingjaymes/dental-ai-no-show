import streamlit as st
import pandas as pd

# ----------------------------
# Streamlit Page Setup (FIRST)
# ----------------------------
st.set_page_config(
    page_title="Dental AI Dashboard",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Load Appointments (CSV for demo)
# ----------------------------
df = pd.read_csv("sample_appointments.csv", parse_dates=["date_time"])

# ----------------------------
# Dashboard Title
# ----------------------------
st.title("🦷 Dental AI - No-Show Risk Dashboard")

# ----------------------------
# Demo Summary Section
# ----------------------------
st.subheader("📊 Demo Summary")
total_appointments = len(df)
high_risk = len(df[df['risk_level']=='High'])
medium_risk = len(df[df['risk_level']=='Medium'])
low_risk = len(df[df['risk_level']=='Low'])

st.markdown(f"""
- Total appointments: **{total_appointments}**  
- High risk (likely no-show): **{high_risk}**  
- Medium risk: **{medium_risk}**  
- Low risk: **{low_risk}**  
""")

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filters")
risk_filter = st.sidebar.multiselect(
    "Select Risk Level",
    options=df['risk_level'].unique(),
    default=df['risk_level'].unique()
)
day_filter = st.sidebar.multiselect(
    "Select Day of Week",
    options=df['date_time'].dt.day_name().unique(),
    default=df['date_time'].dt.day_name().unique()
)

# ----------------------------
# Filter DataFrame
# ----------------------------
df['day_name'] = df['date_time'].dt.day_name()
filtered_df = df[
    (df['risk_level'].isin(risk_filter)) &
    (df['day_name'].isin(day_filter))
]

# ----------------------------
# Show Filtered Appointments
# ----------------------------
st.subheader(f"Upcoming Appointments ({len(filtered_df)})")
st.dataframe(filtered_df[['appointment_id','patient_id','date_time','risk_score','risk_level','appointment_type']])

# ----------------------------
# Highlight High-Risk Appointments
# ----------------------------
st.subheader("⚠️ High-Risk Appointments")
high_risk_df = filtered_df[filtered_df['risk_level']=='High']
st.dataframe(high_risk_df[['appointment_id','patient_id','date_time','risk_score','appointment_type']])