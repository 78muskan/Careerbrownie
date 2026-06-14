from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def split_text(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def join_text(values: list[str]) -> str:
    return ", ".join(item.strip() for item in values if item.strip())
