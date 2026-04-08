from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

async def send_reset_email(email: str, token: str):
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    message = MessageSchema(
        subject="Reset Your Password",
        recipients=[email],
        body=f"Click this link to reset your password:\n\n{reset_link}\n\nThis link expires in 30 minutes.",
        subtype=MessageType.plain,
    )
    fm = FastMail(conf)
    await fm.send_message(message)