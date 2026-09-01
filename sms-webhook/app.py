import os
from urllib.parse import urlencode

import requests
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="SMS Webhook",
    docs_url=None,
    redoc_url=None,
)


API_KEY = os.environ["SMS_WEBHOOK_API_KEY"]

SMS_USERNAME = os.environ["SMS_USERNAME"]
SMS_PASSWORD = os.environ["SMS_PASSWORD"]
SMS_FROM = os.environ["SMS_FROM"]
SMS_PANEL_URL = os.environ["SMS_PANEL_URL"]

SMS_TO = [
    phone.strip()
    for phone in os.environ["SMS_TO"].split(",")
    if phone.strip()
]


class SMSRequest(BaseModel):
    message: str


def set_sms_log(message, phone):
    print(f"sms_log phone={phone} message={message}")


def try_sms(phone, message):
    try:
        url = SMS_PANEL_URL

        payload = {
            "username": SMS_USERNAME,
            "password": SMS_PASSWORD,
            "from": SMS_FROM,
            "to": phone,
            "text": message,
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(
            url,
            headers=headers,
            data=urlencode(payload),
            timeout=10,
        )

        set_sms_log(
            message=message,
            phone=phone,
        )

        print("resp", response.text)

        response.raise_for_status()

    except Exception as ex:
        print("sms_exception", ex)
        return False

    return True


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/alert")
def send_sms(
    data: SMSRequest,
    x_api_key: str = Header(...),
):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
        )

    results = [
        try_sms(phone=phone, message=data.message)
        for phone in SMS_TO
    ]

    if not SMS_TO or not all(results):
        raise HTTPException(
            status_code=502,
            detail="SMS provider failed",
        )

    return {
        "success": True
    }
