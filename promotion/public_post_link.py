"""Strict parser for public Telegram channel-post links.

Private invite links and internal /c/ links are intentionally not accepted.
This module does not fetch content or create views.
"""
from dataclasses import dataclass
from urllib.parse import urlsplit
import re


_USERNAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]{4,31}$")
_MESSAGE_ID_RE = re.compile(r"^[1-9][0-9]*$")
_ALLOWED_HOSTS = {"t.me", "telegram.me", "www.t.me", "www.telegram.me"}


@dataclass(frozen=True)
class PublicPostLink:
    username: str
    message_id: int
    canonical_url: str


def parse_public_post_link(value: str) -> PublicPostLink:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("A public Telegram post link is required.")

    raw = value.strip()
    if "://" not in raw:
        raw = "https://" + raw

    parsed = urlsplit(raw)
    if parsed.scheme != "https" or (parsed.hostname or "").lower() not in _ALLOWED_HOSTS:
        raise ValueError("Use a secure public t.me or telegram.me post link.")

    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(parts) == 3 and parts[0].lower() == "s":
        _, username, message_id_text = parts
    elif len(parts) == 2:
        username, message_id_text = parts
    else:
        raise ValueError("Use a public post link like https://t.me/channelname/123.")

    if username.lower() in {"c", "joinchat"} or username.startswith("+"):
        raise ValueError("Private channel links are not supported in this pilot.")
    if not _USERNAME_RE.fullmatch(username):
        raise ValueError("The channel username in this link is invalid.")
    if not _MESSAGE_ID_RE.fullmatch(message_id_text):
        raise ValueError("The post ID in this link is invalid.")

    message_id = int(message_id_text)
    return PublicPostLink(
        username=username,
        message_id=message_id,
        canonical_url=f"https://t.me/{username}/{message_id}",
    )
