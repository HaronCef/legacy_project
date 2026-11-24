# tests for notify.py (П8, reengineering)
# no real e-mails are sent: send_email is replaced with mock
from unittest.mock import patch

from src import notify


def test_notify_user_order_confirmed():
    with patch.object(notify, "send_email", return_value=True) as m:
        notify.notify_user(1, 1, {"email": "a@test.com", "order_id": 7})
    m.assert_called_once_with("a@test.com", "Order Confirmed",
                              "Your order #7 has been confirmed.")


def test_notify_user_payment_received():
    with patch.object(notify, "send_email", return_value=True) as m:
        notify.notify_user(1, 2, {"email": "a@test.com", "amount": 150})
    m.assert_called_once_with("a@test.com", "Payment Received",
                              "Payment of 150 UAH received.")


def test_notify_user_order_cancelled():
    with patch.object(notify, "send_email", return_value=True) as m:
        notify.notify_user(1, 3, {"email": "a@test.com", "order_id": 9})
    m.assert_called_once_with("a@test.com", "Order Cancelled",
                              "Your order #9 was cancelled.")


def test_notify_user_unknown_type_sends_nothing():
    with patch.object(notify, "send_email") as m:
        notify.notify_user(1, 99, {"email": "a@test.com"})
    m.assert_not_called()


def test_bulk_notify_all_sent():
    users = [{"email": "a@test.com"}, {"email": "b@test.com"}]
    with patch.object(notify, "send_email", return_value=True):
        result = notify.bulk_notify(users, "Promo")
    assert result["sent"] == 2
    assert result["failed"] == 0


def test_send_email_stub_returns_true():
    assert notify.send_email("a@test.com", "Hi", "Body") is True


def test_build_message_unknown_type():
    assert notify.build_message(99, {}) is None


def test_build_message_order_confirmed():
    assert notify.build_message(1, {"order_id": 5}) == (
        "Order Confirmed", "Your order #5 has been confirmed.")


def test_retry_then_success():
    # first attempt fails, second is ok -> message counts as sent
    with patch.object(notify, "send_email", side_effect=[Exception("err"), True]) as m:
        result = notify.bulk_notify([{"email": "a@test.com"}], "Promo")
    assert m.call_count == 2
    assert result == {"sent": 1, "failed": 0, "failed_emails": []}


def test_all_attempts_fail():
    with patch.object(notify, "send_email", side_effect=[Exception("err")] * 3) as m:
        result = notify.bulk_notify([{"email": "a@test.com"}], "Promo")
    assert m.call_count == 3
    assert result == {"sent": 0, "failed": 1, "failed_emails": ["a@test.com"]}


def test_send_returns_false_counts_as_failed():
    with patch.object(notify, "send_email", return_value=False):
        assert notify.send_with_retry("a@test.com", "Hi", "Body") is False
