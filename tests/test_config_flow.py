from aiohttp import ClientError
from unittest.mock import MagicMock

from homeassistant.data_entry_flow import FlowResultType

from custom_components.nodeping_status.config_flow import NodePingConfigFlow
from custom_components.nodeping_status.const import CONF_REPORT_ID, DOMAIN

from .conftest import MOCK_REPORT_ID, mock_aiohttp

_MODULE = "custom_components.nodeping_status.config_flow"


def _make_flow(existing_report_ids: list[str] | None = None) -> NodePingConfigFlow:
    flow = NodePingConfigFlow()
    flow.hass = MagicMock()
    flow.handler = DOMAIN
    flow.context = {"source": "user"}
    flow.flow_id = "test-flow"

    existing = [
        MagicMock(data={CONF_REPORT_ID: rid}) for rid in (existing_report_ids or [])
    ]
    flow.hass.config_entries.async_entries.return_value = existing
    return flow


async def test_form_shown() -> None:
    result = await _make_flow().async_step_user(None)
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"
    assert not result["errors"]


async def test_create_entry() -> None:
    with mock_aiohttp(_MODULE, status=200):
        result = await _make_flow().async_step_user(
            {CONF_REPORT_ID: MOCK_REPORT_ID, "name": "My NodePing"}
        )

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "My NodePing"
    assert result["data"] == {CONF_REPORT_ID: MOCK_REPORT_ID}


async def test_invalid_report_id() -> None:
    with mock_aiohttp(_MODULE, status=404):
        result = await _make_flow().async_step_user(
            {CONF_REPORT_ID: "badid", "name": "Bad"}
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {CONF_REPORT_ID: "invalid_report_id"}


async def test_cannot_connect_http_error() -> None:
    with mock_aiohttp(_MODULE, status=503):
        result = await _make_flow().async_step_user(
            {CONF_REPORT_ID: MOCK_REPORT_ID, "name": "Test"}
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}


async def test_cannot_connect_network_error() -> None:
    with mock_aiohttp(_MODULE, exception=ClientError("err")):
        result = await _make_flow().async_step_user(
            {CONF_REPORT_ID: MOCK_REPORT_ID, "name": "Test"}
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}


async def test_already_configured() -> None:
    from homeassistant.data_entry_flow import AbortFlow

    with mock_aiohttp(_MODULE, status=200):
        try:
            await _make_flow(existing_report_ids=[MOCK_REPORT_ID]).async_step_user(
                {CONF_REPORT_ID: MOCK_REPORT_ID, "name": "Duplicate"}
            )
            assert False, "Expected AbortFlow"
        except AbortFlow as exc:
            assert exc.reason == "already_configured"
