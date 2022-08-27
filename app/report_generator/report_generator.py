import urllib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from botocore.client import BaseClient
from smtplib import SMTP_SSL
from typing import Any, Dict

from app.report_generator.constants import EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT
from app.report_generator.utils import transform_csv_object_to_transactions, get_transactions_html_report, \
    get_transactions_summary


class ReportGenerator:

    def __init__(self, s3_client: BaseClient, smtp_client: SMTP_SSL):
        self.s3 = s3_client
        self.smtp = smtp_client

    def generate_report(self, event: Any, context: Any):
        original_data = self._get_data(event)
        processed_data = self._process_data(original_data)
        self._send_report(processed_data)

    def _get_data(self, event: Any) -> Any:
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")
        csv_object = self.s3.get_object(Bucket=bucket, Key=key)
        return transform_csv_object_to_transactions(csv_object)

    def _process_data(self, data: Any) -> Dict:
        return get_transactions_summary(data)

    def _send_report(self, context: Dict):
        body = get_transactions_html_report(context)

        message = MIMEMultipart("alternative")
        message["Subject"] = EMAIL_SUBJECT
        message["From"] = EMAIL_FROM
        message["To"] = EMAIL_TO
        message.attach(MIMEText(body, "html"))

        self.smtp.sendmail(EMAIL_FROM, EMAIL_TO, message.as_string())
