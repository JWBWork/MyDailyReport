import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from loguru import logger

def send_email(subject: str, email_address: str, token: str):
    verification_href = f"https://localhost:9000/user?verification_token={token}"
    message = Mail(
        from_email='verification@mydaily.report',
        to_emails=email_address,
        subject=subject,
        html_content='<strong>Welcome to MyDailyReport!</strong>'\
            f'<br/><a href="{verification_href}">Please click to verify your email!</a>'
    )
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    logger.info(f"Email sent to {email_address=} with {response=}")
    return response
