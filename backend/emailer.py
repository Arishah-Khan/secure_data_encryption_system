import smtplib
from email.message import EmailMessage
import streamlit as st

def send_email(to_email, passkey):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Your Secure Decryption Key"
        msg["From"] = st.secrets["SENDER_EMAIL"] 
        msg["To"] = to_email
        msg.set_content(f"Your passkey is: {passkey}")

        # Connect to SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(st.secrets["SENDER_EMAIL"], st.secrets["SENDER_PASSWORD"])  
            smtp.send_message(msg)

        return "email_sent"

    except smtplib.SMTPAuthenticationError:
        return "auth_error" 

    except smtplib.SMTPRecipientsRefused:
        return "invalid_recipient"  

    except smtplib.SMTPException as e:
        return f"smtp_error: {str(e)}" 

    except Exception as e:
        return f"unexpected_error: {str(e)}"  
