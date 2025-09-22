from fastapi import APIRouter
import smtplib
from email.message import EmailMessage
from mail.model import Email
from config import setting
emailRouter = APIRouter(prefix="/email", tags=['email'])

@emailRouter.post('/')
async def sendEmail(email: Email):
    msg = EmailMessage()
    msg["to"] = "admin@yitro-consulting.com"
    msg["from"] = email.sender
    msg["Subject"] = email.subject + ", de la part de "+email.name
    msg.set_content = email.content
    
    with smtplib.SMTP_SSL("node125-eu.n0c.com", 465) as smtp:
        smtp.login(setting.email, setting.password)
        smtp.send_message(msg)
        return {
            "message": "email sent"
        }
    return {
        "message": "email not sent"
    }