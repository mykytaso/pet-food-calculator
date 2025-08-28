import time
from datetime import timedelta

import requests
from celery import shared_task
from django.utils.timezone import now

from PetFoodCalculator import settings


MESSAGE_TITLE = "<b>🐱 Pet Food Calculator</b>\n"


def send_telegram_message(message: str) -> None:
    url = f"https://api.telegram.org/bot{getattr(settings, 'TELEGRAM_BOT_TOKEN')}/sendMessage"

    payload = {
        "chat_id": getattr(settings, "TELEGRAM_CHAT_ID"),
        "text": message,
        "parse_mode": "HTML",
    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        raise Exception(f"Error sending message: {response.text}")


@shared_task
def tm_new_user_created(date_joined, email: str) -> None:
    send_telegram_message(
        f"{MESSAGE_TITLE}"
        f"⏱️ {(date_joined - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"👨‍🦰 <b>New User Registered</b>\n"
        f"📧 {email}"
    )


@shared_task
def tm_user_visited_bmc_first_time(email: str) -> None:
    send_telegram_message(
        f"{MESSAGE_TITLE}"
        f"⏱️ {(now() - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"👨‍🦰 <b>User Visited ☕️BMC the first time</b>\n"
        f"📧 {email}"
    )


@shared_task
def tm_user_visited_bmc_again(email: str) -> None:
    send_telegram_message(
        f"{MESSAGE_TITLE}"
        f"⏱️ {(now() - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"👨‍🦰 <b>User Visited ☕️BMC again</b>\n"
        f"📧 {email}"
    )


@shared_task
def tm_guest_visited_bmc_first_time():
    send_telegram_message(
        f"{MESSAGE_TITLE}"
        f"⏱️ {(now() - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"👻 <b>Guest Visited ☕️BMC</b>\n"
    )


@shared_task
def tm_send_message(email: str, message: str) -> None:
    send_telegram_message(
        f"{MESSAGE_TITLE}"
        f"⏱️ {(now() - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"📧 <b>Message from: {email}</b>\n"
        f"💬 {message}"
    )
