#!/usr/bin/python3

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os
import logging

RESULT_DIR = './result'
EMAIL_TITLE = "豆瓣每日日报"
EMAIL_FROM = "**"
EMAIL_PASSWORD = "**"
EMAIL_TO = ["**"]
EMAIL_HOST = "**"
EMAIL_PORT = 465
EMAIL_MESSAGE = "豆瓣每日日报见附件"


def init_log():
    log_format = '[%(asctime)-15s] %(message)s'
    logging.basicConfig(format=log_format)
    return logging.getLogger()


def read_message_content():
    with open(os.path.join(RESULT_DIR, "latest.html")) as file:
        return file.read()


def send_email():
    message = MIMEMultipart()
    message["Subject"] = Header(EMAIL_TITLE)
    message["From"] = Header(EMAIL_FROM)
    message["To"] = Header(";".join(EMAIL_TO))
    message.attach(MIMEText(EMAIL_MESSAGE, "plain", "utf-8"))

    attachment = MIMEText(read_message_content(), 'base64', 'utf-8')
    attachment["Content-Type"] = "application/octet-stream"
    attachment["Content-Disposition"] = 'attachment; filename="latest.html"'
    message.attach(attachment)

    smtpObj = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
    smtpObj.login(EMAIL_FROM, EMAIL_PASSWORD)
    smtpObj.sendmail(EMAIL_FROM, EMAIL_TO, message.as_string())


def main():
    logger = init_log()
    logger.setLevel("INFO")

    logger.info("start to send email...")
    send_email()
    logger.info("send email successfully...")


if __name__ == "__main__":
    main()
