import re
import urllib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from typing import Any, Dict

from botocore.client import BaseClient

from .constants import DEFAULT_EMAIL_TO, EMAIL_FROM, EMAIL_SUBJECT
from .utils import (
    get_transactions_html_report,
    get_transactions_summary,
    is_valid_email,
    transform_csv_object_to_transactions,
)


class ReportGenerator:
    """this function gets data from a given S3 bucket, process the data and creates a summary.
        If a correct email is provided it sends a summary to the user.
        Otherwise, it sends a summary to the default email.

    Attributes:
        s3_client (BaseClient): The Boto S3 client.
        smtp_client (SMTP): The SMTP client.
    """

    def __init__(self, s3_client: BaseClient, smtp_client: SMTP):
        self.s3 = s3_client
        self.smtp = smtp_client

    def generate_report(self, event: Any, context: Any):
        original_data = self._get_data(event)
        processed_data = self._process_data(original_data)
        self._send_report(event, processed_data)

    def _get_data(self, event: Any) -> Any:
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(
            event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
        )
        csv_object = self.s3.get_object(Bucket=bucket, Key=key)
        return transform_csv_object_to_transactions(csv_object)

    # ToDo: Inject data processor and data getter to handle different reports.
    def _process_data(self, data: Any) -> Dict:
        return get_transactions_summary(data)

    def _send_report(self, event: Any, context: Dict):
        key = urllib.parse.unquote_plus(
            event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
        )
        user_provided_email = re.search(r"txn\/(.*).csv", key, re.IGNORECASE).group(1)
        email_to = (
            user_provided_email
            if is_valid_email(user_provided_email)
            else DEFAULT_EMAIL_TO
        )

        body = get_transactions_html_report(context)

        message = MIMEMultipart("alternative")
        message["Subject"] = EMAIL_SUBJECT
        message["From"] = EMAIL_FROM
        message["To"] = email_to
        message.attach(MIMEText(body, "html"))

        self.smtp.sendmail(EMAIL_FROM, email_to, message.as_string())
