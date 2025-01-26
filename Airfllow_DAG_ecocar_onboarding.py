from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import json
import os
import smtplib
from email.mime.text import MIMEText
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load Google API credentials
CREDENTIALS_FILE = "/opt/airflow/dags/service_credentials.json"

# Load email sender credentials
EMAIL_SENDER = "your-email-here"
EMAIL_PASSWORD = "your-app-password"

# Google Sheets details
SHEET_ID = "your_google_sheets_id"
RANGE_NAME = "Sheet1!A:D"

# DAG Configuration
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "ecocar_onboarding",
    default_args=default_args,
    description="Automates the onboarding process for EcoCAR team",
    schedule_interval=timedelta(days=1),  # Runs daily
)

# Function to Read Google Sheets
def read_google_sheets():
    creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE_NAME).execute()
    values = result.get("values", [])
    return values

# Function to Send Leader Approval Request
def send_approval_request():
    data = read_google_sheets()
    for row in data[1:]:  # Skip headers
        name, email, status, role = row
        if status.lower() == "pending":
            msg = MIMEText(f"Hello,\n\nPlease approve or decline {name}'s onboarding request.\n\nReply with 'Approve' or 'Reject'.")
            msg["Subject"] = f"Onboarding Request: {name}"
            msg["From"] = EMAIL_SENDER
            msg["To"] = "leader@example.com"

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.sendmail(EMAIL_SENDER, "leader@example.com", msg.as_string())

# Function to Process Leader Responses
def process_responses():
    data = read_google_sheets()
    updated_data = []

    for row in data[1:]:
        name, email, status, role = row
        if status.lower() == "approve":
            send_onboarding_email(email, name)
            updated_data.append([name, email, "Approved", role])
        elif status.lower() == "reject":
            send_rejection_email(email, name)
            updated_data.append([name, email, "Rejected", role])
        else:
            updated_data.append(row)

    update_google_sheets(updated_data)

# Function to Send Onboarding Email
def send_onboarding_email(email, name):
    msg = MIMEText(f"Hello {name},\n\nCongratulations! You have been approved to join the EcoCAR team.")
    msg["Subject"] = "Welcome to EcoCAR!"
    msg["From"] = EMAIL_SENDER
    msg["To"] = email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, email, msg.as_string())

# Function to Send Rejection Email
def send_rejection_email(email, name):
    msg = MIMEText(f"Hello {name},\n\nUnfortunately, your application to join the EcoCAR team was not approved.")
    msg["Subject"] = "EcoCAR Application Status"
    msg["From"] = EMAIL_SENDER
    msg["To"] = email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, email, msg.as_string())

# Function to Update Google Sheets with Final Decisions
def update_google_sheets(data):
    creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    
    body = {"values": [["Name", "Email", "Status", "Role"]] + data}
    sheet.values().update(
        spreadsheetId=SHEET_ID,
        range=RANGE_NAME,
        valueInputOption="RAW",
        body=body
    ).execute()

# Airflow Tasks
task1 = PythonOperator(
    task_id="send_approval_request",
    python_callable=send_approval_request,
    dag=dag,
)

task2 = PythonOperator(
    task_id="process_responses",
    python_callable=process_responses,
    dag=dag,
)

# Task Dependencies
task1 >> task2
