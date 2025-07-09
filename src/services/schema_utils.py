from datetime import UTC, datetime
from typing import Any


def make_error_payload(
    code: str,
    detail: str,
    meta: dict[str, Any] | None = None,
) -> dict:
    base_meta = {
        "timestamp": datetime.now(UTC).isoformat(),
    }
    if meta:
        base_meta.update(meta)

    return {
        "type": "error",
        "payload": {
            "code": code,
            "detail": detail,
        },
        "meta": base_meta,
    }
