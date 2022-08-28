import os
import boto3
from smtplib import SMTP_SSL

from report_generator.report_generator import ReportGenerator


# Create shared S3 client to get input
s3 = boto3.client('s3')

# Create shared smtp client to send email
smtp_ssl = SMTP_SSL(os.getenv("EMAIL_HOST"))
smtp_ssl.starttls()
smtp_ssl.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))

# Report generator instance to process events
report_generator = ReportGenerator(s3, smtp_ssl)


def lambda_handler(event, context):
    report_generator.generate_report(event, context)
