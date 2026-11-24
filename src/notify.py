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

# message types: new type = one new line here
MAX_RETRIES = 2  # extra attempts after the first one

ORDER_CONFIRMED = 1
PAYMENT_RECEIVED = 2
ORDER_CANCELLED = 3

MESSAGES = {
    ORDER_CONFIRMED: ("Order Confirmed", "Your order #{order_id} has been confirmed."),
    PAYMENT_RECEIVED: ("Payment Received", "Payment of {amount} UAH received."),
    ORDER_CANCELLED: ("Order Cancelled", "Your order #{order_id} was cancelled."),
}


def send_email(to, subj, body):
    print(f"[STUB] Would send email to {to}: {subj}")
    return True


def send_with_retry(to, subj, body):
    """Try to send a message, on error try again MAX_RETRIES times. Returns True if sent."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            if send_email(to, subj, body):
                return True
        except Exception as e:  # pylint: disable=broad-exception-caught
            # any error of the mail channel means "try again"
            log_notification(to, subj, f"error on attempt {attempt + 1}: {e}")
    return False


def build_message(msg_type, data):
    """Return (subject, body) for msg_type, or None if the type is unknown."""
    if msg_type not in MESSAGES:
        return None
    subj, template = MESSAGES[msg_type]
    body = template.format(order_id=data.get("order_id"), amount=data.get("amount"))
    return subj, body


def notify_user(user_id, msg_type, data=None):
    """Send a notification of msg_type to the user."""
    data = data or {}
    message = build_message(msg_type, data)
    if message is None:
        return
    send_with_retry(data.get("email", ""), message[0], message[1])


def bulk_notify(users, msg):
    """Send the same message to many users. Returns counts and list of failed e-mails."""
    result = {"sent": 0, "failed": 0, "failed_emails": []}
    for u in users:
        email = u.get("email", "")
        if send_with_retry(email, "Notification", msg):
            result["sent"] += 1
        else:
            result["failed"] += 1
            result["failed_emails"].append(email)
    return result


def log_notification(user_id, tp, status):
    # TODO: write to DB (never implemented)
    pass
