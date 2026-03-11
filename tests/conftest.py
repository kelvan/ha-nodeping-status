from contextlib import contextmanager
from unittest.mock import AsyncMock, MagicMock, patch

MOCK_REPORT_ID = "testrepid123"

MOCK_API_RESPONSE = {
    "jobs": [
        {
            "_id": "check001",
            "label": "My Website",
            "type": "HTTPADV",
            "status": "up",
            "lastmessage": "Connection accepted",
            "rt": 145,
            "uptime": {
                "2025-01-15": {"uptime": 99.9},
                "total": {"uptime": 99.5},
            },
        },
        {
            "_id": "check002",
            "label": "My API",
            "type": "HTTP",
            "status": "down",
            "lastmessage": "Connection refused",
            "uptime": {
                "2025-01-15": {"uptime": 95.0},
                "total": {"uptime": 98.2},
            },
        },
    ]
}


@contextmanager
def mock_aiohttp(module: str, status: int = 200, payload=None, exception=None):
    if exception is not None:
        cm = MagicMock()
        cm.__aenter__ = AsyncMock(side_effect=exception)
        cm.__aexit__ = AsyncMock(return_value=False)
    else:
        resp = MagicMock()
        resp.status = status
        resp.json = AsyncMock(return_value=payload or {})
        resp.__aenter__ = AsyncMock(return_value=resp)
        resp.__aexit__ = AsyncMock(return_value=False)
        cm = resp

    session = MagicMock()
    session.get = MagicMock(return_value=cm)
    with patch(f"{module}.async_get_clientsession", return_value=session):
        yield
