# notify.py
# Notification system
# DEPRECATED - use new_notify.py (which doesn't exist yet)
# kept for reference

import os

# SMTP settings are read from environment variables, not stored in code
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")


def send_email(to, subj, body):
    print(f"[STUB] Would send email to {to}: {subj}")
    return True


def notify_user(user_id, msg_type, data=None):
    # types: 1=order_confirmed, 2=payment_received, 3=order_cancelled
    if msg_type == 1:
        send_email(
            data.get('email', ''),
            "Order Confirmed",
            f"Your order #{data.get('order_id')} has been confirmed."
        )
    elif msg_type == 2:
        send_email(
            data.get('email', ''),
            "Payment Received",
            f"Payment of {data.get('amount')} UAH received."
        )
    elif msg_type == 3:
        send_email(
            data.get('email', ''),
            "Order Cancelled",
            f"Your order #{data.get('order_id')} was cancelled."
        )


def bulk_notify(users, msg):
    # used once in 2021 for promo campaign, kept just in case
    sent = 0
    failed = 0
    for u in users:
        try:
            send_email(u.get('email', ''), "Notification", msg)
            sent += 1
        except Exception:
            failed += 1
    return {"sent": sent, "failed": failed}


def log_notification(user_id, tp, status):
    # TODO: write to DB (never implemented)
    pass
