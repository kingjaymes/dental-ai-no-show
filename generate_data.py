import pandas as pd
import random
from datetime import datetime, timedelta

num_appointments = 500
appointment_types = ['Cleaning', 'Extraction', 'Consultation', 'Whitening']

data = []

for i in range(1, num_appointments+1):
    appointment_date = datetime.now() + timedelta(days=random.randint(1, 30))
    booking_lead = random.randint(1, 30)
    past_misses = random.randint(0, 5)
    app_type = random.choice(appointment_types)
    
    data.append({
        'patient_id': i,
        'date_time': appointment_date.strftime('%Y-%m-%d %H:%M:%S'),
        'appointment_type': app_type,
        'past_attendance': past_misses,
        'booking_lead_time': booking_lead
    })

df = pd.DataFrame(data)
df.to_csv('sample_appointments.csv', index=False)

print("Sample appointments CSV created successfully.")