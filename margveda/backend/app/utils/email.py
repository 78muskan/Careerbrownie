import logging


logger = logging.getLogger(__name__)


def send_email(to_email: str, subject: str, body: str) -> None:
    # In production this function can call SendGrid, SES, SMTP, or another provider.
    logger.info("Email queued | to=%s | subject=%s | body=%s", to_email, subject, body)
