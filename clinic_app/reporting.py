
# import smtplib
# from email.message import EmailMessage
# import os
# from pathlib import Path
# from  dotenv import load_dotenv

# current_dir = Path(__file__).parent
# env_path = current_dir.parent / '.env'
# load_dotenv(dotenv_path=env_path)
# patient_mail=""
# def login_to_database(name,recipient_email):
#     patient_mail=recipient_email
#     SENDER_EMAIL = os.getenv("EMAIL")
#     SENDER_PASSWORD = os.getenv("PASSWORD")
#     body = f'''Welcome  Jeevdhaan Hospital Mr.{name}
#     Have a Great Treatment with out Doctors.
#     '''
#     if not SENDER_EMAIL or not SENDER_PASSWORD:
#          return False
#     msg = EmailMessage()
#     msg["Subject"] = "About the login info"
#     msg["From"] = "Jeevdhaan Hospital"
#     msg["To"] = recipient_email
#     msg.set_content(body)
#     try:
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(SENDER_EMAIL, SENDER_PASSWORD)
#             server.send_message(msg)
#             return True
#     except Exception:
#         return False


      
# def send_patient_email(patient_record):
#     """Constructs and sends a patient report email."""
    
#     # Securely get sender credentials from environment variables
#     SENDER_EMAIL = os.getenv("SENDER_EMAIL")
#     SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

#     if not SENDER_EMAIL or not SENDER_PASSWORD:
#         print("\n--- Email Sending Skipped: SENDER_EMAIL or SENDER_PASSWORD not set. ---")
#         return False

#     # CORRECT: Get the recipient's email from the patient's owner
#     recipient_email = patient_record.owner.email
#     if not recipient_email:
#         print(f"--- Email Sending Skipped: Patient ID {patient_record.id} has no owner email. ---")
#         return False

#     # Create a personalized subject and body
#     email_subject = f"Your Clinic Report for Patient ID: {patient_record.id}"
#     email_body = f"""
#     Hello {patient_record.owner.name or 'User'},

#     This is a notification from our clinic with a summary of the patient's details:

#     - Patient ID:     {patient_record.id}
#     - Name:           {patient_record.name or 'N/A'}
#     - Age:            {patient_record.age or 'N/A'}
#     - Mobile Number:  {patient_record.phone or 'N/A'}
#     - Disease:        {patient_record.disease or 'N/A'}
#     - Description:    {patient_record.description or 'N/A'}

#     Please keep this for your records.

#     Best regards,
#     The Clinic
#     """