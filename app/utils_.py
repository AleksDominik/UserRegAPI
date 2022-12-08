import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import emails
from emails.template import JinjaTemplate
from jose import jwt

from core.config import settings
import os
import string, secrets

# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

templates_ids={
    'new_account':'d-653b2469d60f4c96b37532599e7f1573',
    'reset_password':'d-b683da0f5587483faa382babf1b54935',
    'test':'d-f8676e3681a74879b006024447122475'
}
 
def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
    template_id:str='test'
) -> None:
    print(settings.EMAILS_ENABLED)
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    print('the email has been sent to {email_to}')
    print(environment)

def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    print('test email')
    # subject = f"{project_name} - Test email"
    # with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
    #     template_str = f.read()
    # send_email(
    #     email_to=email_to,
    #     subject_template=subject,
    #     html_template=template_str,
    #     environment={"project_name": settings.PROJECT_NAME, "email": email_to},

    # )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    print('reset email')
    # subject = f"{project_name} - Password recovery for user {email}"

    # server_host = settings.SERVER_HOST
    # link = f"{server_host}/reset-password?token={token}"
    # send_email(
    #     email_to=email_to,
    #     subject_template=subject,
    #     environment={
    #         "project_name": settings.PROJECT_NAME,
    #         "username": email,
    #         "email": email_to,
    #         "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
    #         "link": link,
    #     },
    #     template_id='reset_password'
    # )


def send_new_account_email(email_to: str, password: str) -> None:
    print(f'new account email to {email_to} the password is {password} you have 4 minute to activate the account')
    # project_name = settings.PROJECT_NAME
    # subject = f"{project_name} - New account for user {username}"

    # link = settings.SERVER_HOST
    # send_email(
    #     email_to=email_to,
    #     environment={
    #         "project_name": settings.PROJECT_NAME,
    #         "username": username,
    #         "password": password,
    #         "email": email_to,
    #         "link": link,
    #     },
    #     template_id='new_account'

    # )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "email": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None
def generate_password(length= 4):
    alphabet = string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))