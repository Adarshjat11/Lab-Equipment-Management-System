import smtplib
from email.message import EmailMessage
from datetime import datetime
import streamlit as st

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

def send_issue_email(student, email, semester, equipment, qty):
    msg = EmailMessage()
    msg["Subject"] = "Lab Equipment Issued"
    msg["From"] = st.secrets["SENDER_EMAIL"]
    msg["To"] = st.secrets["ADMIN_EMAIL"]

    msg.set_content(f"""
New Equipment Issued

Student Name : {student}
Student Email: {email}
Semester     : {semester}

Equipment    : {equipment}
Quantity     : {qty}
Time         : {datetime.now().strftime('%Y-%m-%d %H:%M')}
""")

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(
            st.secrets["SENDER_EMAIL"],
            st.secrets["SENDER_PASSWORD"]
        )
        server.send_message(msg)
