from aiohttp import ClientError
from unittest.mock import MagicMock

from custom_components.nodeping_status.coordinator import NodePingCoordinator

from .conftest import MOCK_API_RESPONSE, MOCK_REPORT_ID, mock_aiohttp

_MODULE = "custom_components.nodeping_status.coordinator"


def _make_coordinator() -> NodePingCoordinator:
    coordinator = NodePingCoordinator.__new__(NodePingCoordinator)
    coordinator.hass = MagicMock()
    coordinator.report_id = MOCK_REPORT_ID
    return coordinator


async def test_fetch_data() -> None:
    coordinator = _make_coordinator()
    with mock_aiohttp(_MODULE, payload=MOCK_API_RESPONSE):
        result = await coordinator._async_update_data()

    assert "check001" in result
    assert result["check001"]["label"] == "My Website"
    assert result["check001"]["status"] == "up"
    assert "check002" in result
    assert result["check002"]["status"] == "down"


async def test_empty_jobs() -> None:
    coordinator = _make_coordinator()
    with mock_aiohttp(_MODULE, payload={"jobs": []}):
        result = await coordinator._async_update_data()

    assert result == {}


async def test_http_error() -> None:
    from homeassistant.helpers.update_coordinator import UpdateFailed

    coordinator = _make_coordinator()
    with mock_aiohttp(_MODULE, status=500):
        try:
            await coordinator._async_update_data()
            assert False, "Expected UpdateFailed"
        except UpdateFailed:
            pass


async def test_connection_error() -> None:
    from homeassistant.helpers.update_coordinator import UpdateFailed

    coordinator = _make_coordinator()
    with mock_aiohttp(_MODULE, exception=ClientError("connection error")):
        try:
            await coordinator._async_update_data()
            assert False, "Expected UpdateFailed"
        except UpdateFailed:
            pass
