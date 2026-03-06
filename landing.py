import streamlit as st

st.set_page_config(page_title="Opalon AI", layout="wide")

st.title("🦷 Opalon AI")
st.subheader("Reduce Dental Appointment No-Shows with AI")

st.write("""
Dental clinics lose thousands every month due to missed appointments.

Opalon AI predicts which patients are most likely to miss appointments so clinics
can send targeted reminders and recover lost revenue.
""")

st.markdown("---")

st.header("📊 Live Demo")
st.write("Use the sidebar on the left to open the Dashboard Demo.")

st.header("Who This Is For")
st.write("""
• Dental clinics  
• Practice managers  
• Multi-location dental groups
""")

st.header("Contact")
st.write("Email: **opalondental@gmail.com**")
st.write("Connect on LinkedIn **https://www.linkedin.com/in/james-opaluwa-76417a118**")

st.markdown("---")
st.header("💰 Clinic Revenue Loss Calculator")

st.write("""
Estimate how much money your clinic loses each month due to missed appointments
and see how much Opalon AI could help recover.
""")

# Input widgets
appointments_per_week = st.number_input("Number of appointments per week", min_value=1, value=40)
average_appointment_value = st.number_input("Average appointment value ($/£)", min_value=1, value=120)
no_show_rate = st.slider("Estimated no-show rate (%)", min_value=0, max_value=100, value=20)
ai_reduction_pct = st.slider("Expected no-show reduction with Opalon AI (%)", min_value=0, max_value=100, value=30)

# Calculate losses
monthly_appointments = appointments_per_week * 4  # approx 4 weeks
loss_per_month = monthly_appointments * (no_show_rate / 100) * average_appointment_value
recovered_with_ai = loss_per_month * (ai_reduction_pct / 100)

st.markdown("### 💸 Estimated Loss & Recovery")
st.write(f"**Monthly revenue lost due to no-shows:** ${loss_per_month:,.2f}")
st.write(f"**Potential recovered with Opalon AI:** ${recovered_with_ai:,.2f}")