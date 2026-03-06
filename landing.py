import streamlit as st

st.set_page_config(page_title="Dental AI", layout="wide")

st.title("🦷 Dental AI")
st.subheader("Reduce Dental Appointment No-Shows with Artificial Intelligence")

st.write("""
Dental clinics lose thousands every year due to missed appointments.

Dental AI uses **machine learning** to predict which patients are most likely to miss their appointments and helps clinics take action early.
""")

st.header("The Problem")

st.write("""
• Dental clinics lose revenue from missed appointments  
• Staff waste time on manual reminders  
• Schedules become inefficient  
""")

st.header("Our Solution")

st.write("""
Dental AI analyzes appointment data and predicts **no-show risk**.

Clinics can:

• Identify high-risk patients  
• Send targeted reminders  
• Optimize appointment scheduling  
• Reduce no-shows by up to **30%**
""")

st.header("Product Demo")

st.write("See our AI dashboard in action.")

if st.button("Open AI Dashboard Demo"):
    st.switch_page("pages/dashboard.py")

st.header("Who This Is For")

st.write("""
• Dental clinics  
• Dental practice managers  
• Multi-location dental groups
""")

st.header("Contact")

st.write("""
Interested in testing Dental AI?

Email: **opalondental@gmail.com**

Or connect on LinkedIn.
""")

st.success("Dental AI MVP • Built with Python & Machine Learning")