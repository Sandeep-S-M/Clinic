import smtplib
import os
from pathlib import Path
from email.message import EmailMessage
from dotenv import load_dotenv


# Import the SQLAlchemy models from models.py
project_root = Path(__file__).parent.parent.parent
env_path = project_root/ '.env'
# Load environment variables from a .env file

load_dotenv(dotenv_path=env_path)

def send_welcome_email(user):
    
    SENDER_EMAIL = os.getenv("EMAIL")
    SENDER_PASSWORD = os.getenv("PASSWORD")

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("\n--- Welcome Email Skipped: SENDER_EMAIL or SENDER_PASSWORD not set. ---")
        return False

    body = f"""
    Hello {user.name},

    Welcome to Jeevdhaan Hospital! We are glad to have you with us.
    
    You have successfully registered with the email: {user.email}

    Have a great treatment with our doctors.

    Best regards,
    The Clinic
    """
    
    msg = EmailMessage()
    msg["Subject"] = "Welcome to Jeevdhaan Hospital"
    msg["From"] = "Jeevdhaan Hospital"
    msg["To"] = user.email
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print(f"Successfully sent welcome email to {user.email}")
            return True
    except Exception as e:
        print(f"Failed to send welcome email to {user.email}. Error: {e}")
        return False

def send_patient_report_email(patient_record):
    """Constructs and sends a patient report email."""
    
    SENDER_EMAIL = os.getenv("EMAIL")
    SENDER_PASSWORD = os.getenv("PASSWORD")

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("\n--- Patient Report Email Skipped: SENDER_EMAIL or SENDER_PASSWORD not set. ---")
        return False

    recipient_email = patient_record.owner.email
    if not recipient_email:
        print(f"--- Email Sending Skipped: Patient ID {patient_record.id} has no owner email. ---")
        return False

    email_subject = f"Your Clinic Report for Patient ID: {patient_record.id}"
    email_body = f"""
    Hello {patient_record.owner.name or 'User'},

    This is a notification from our clinic with a summary of the patient's details:

    - Patient ID:     {patient_record.id}
    - Name:           {patient_record.name or 'N/A'}
    - Age:            {patient_record.age or 'N/A'}
    - Mobile Number:  {patient_record.phone or 'N/A'}
    - Disease:        {patient_record.disease or 'N/A'}
    - Description:    {patient_record.description or 'N/A'}

    Please keep this for your records.

    Best regards,
    The Clinic
    """

    msg = EmailMessage()
    msg['Subject'] = email_subject
    msg['From'] = "Jeevdhan Hospital"
    msg['To'] = recipient_email
    msg.set_content(email_body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print(f"Successfully sent report to {recipient_email}")
            return True
    except Exception as e:
        print(f"Failed to send email to {recipient_email}. Error: {e}")
        return False

