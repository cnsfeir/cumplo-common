import base64
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import ClassVar

from google.oauth2 import service_account
from googleapiclient.discovery import build
from pydantic import BaseModel

from cumplo_common.utils.constants import GMAIL_CREDENTIALS, GMAIL_FROM_EMAIL, GMAIL_USER_ID


class Attachment(BaseModel):
    """An attachment to an email."""

    path: str
    content_id: str


class Gmail:
    """Integration with Gmail API."""

    SCOPES: ClassVar[list[str]] = ["https://mail.google.com/"]

    @classmethod
    def _authenticate(cls) -> build:
        """Authenticate with Gmail API."""
        credentials = service_account.Credentials.from_service_account_file(
            filename=GMAIL_CREDENTIALS,
            subject=GMAIL_FROM_EMAIL,
            scopes=cls.SCOPES,
        )
        return build("gmail", "v1", credentials=credentials)

    @classmethod
    def get_message(cls, history_id: str) -> dict | None:
        """
        Retrieve the message associated with a specific message history ID.

        Args:
            history_id: The message history ID to look up

        Returns:
            The message data as a dictionary, or None if not found

        """
        service = cls._authenticate()
        response = service.users().history().list(userId=GMAIL_USER_ID, startHistoryId=history_id).execute()

        for history in response.get("history", []):
            for message_added in history.get("messagesAdded", []):
                if message_id := message_added.get("message", {}).get("id"):
                    return service.users().messages().get(userId=GMAIL_USER_ID, id=message_id).execute()

        return None

    @classmethod
    def send_email(cls, to: str, subject: str, content: str, *attachments: Attachment) -> dict:
        """
        Send an HTML email with attachments to a specific email address.

        Args:
            to: The email address to send the email to
            subject: The subject of the email
            content: The content of the email
            *attachments: The attachments to send with the email

        Returns:
            The response from the Gmail API

        """
        message = MIMEMultipart("related")
        message["Subject"] = subject
        message["From"] = GMAIL_FROM_EMAIL
        message["To"] = to

        message.attach(MIMEText(content, "html"))

        for attachment in attachments:
            with Path(attachment.path).open("rb") as file:
                attachment_image = MIMEImage(file.read())
                attachment_image.add_header("Content-ID", f"<{attachment.content_id}>")
                attachment_image.add_header("Content-Disposition", "inline", filename=attachment.path)
                message.attach(attachment_image)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service = cls._authenticate()

        return service.users().messages().send(userId=GMAIL_USER_ID, body={"raw": raw_message}).execute()
