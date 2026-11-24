"""Notifications for users: order e-mails and bulk messages.

Settings come from env variables (see .env.example). Real SMTP sending is
not implemented yet - send_email() is a stub.
"""
import os
import sys

# SMTP settings are read from environment variables, not stored in code
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")

MAX_RETRIES = 2  # extra attempts after the first one

# message types: new type = one new line in MESSAGES
ORDER_CONFIRMED = 1
PAYMENT_RECEIVED = 2
ORDER_CANCELLED = 3

MESSAGES = {
    ORDER_CONFIRMED: ("Order Confirmed", "Your order #{order_id} has been confirmed."),
    PAYMENT_RECEIVED: ("Payment Received", "Payment of {amount} UAH received."),
    ORDER_CANCELLED: ("Order Cancelled", "Your order #{order_id} was cancelled."),
}


def send_email(to, subj, body):  # pylint: disable=unused-argument
    """Send one e-mail. Stub for now: only prints, body is not used yet."""
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
    """Send a notification of msg_type to the user. Returns True if sent."""
    data = data or {}
    message = build_message(msg_type, data)
    if message is None:
        log_notification(user_id, msg_type, "unknown type")
        return False
    ok = send_with_retry(data.get("email", ""), message[0], message[1])
    log_notification(user_id, msg_type, "sent" if ok else "failed")
    return ok


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
    """Write notification status to stderr (saving to DB is not done yet)."""
    print(f"[notify] user={user_id} type={tp} status={status}", file=sys.stderr)
