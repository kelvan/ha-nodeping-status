from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest

from custom_components.nodeping_status.sensor import NodePingUptimeSensor

_UPTIME_DATA = {
    "2025-01-15": {"uptime": 99.9},
    "total": {"uptime": 99.5},
}


def _make_sensor(period: str, uptime: dict = _UPTIME_DATA) -> NodePingUptimeSensor:
    coordinator = MagicMock()
    coordinator.data = {"check001": {"uptime": uptime}}
    return NodePingUptimeSensor(coordinator, "check001", period)


def test_today_uptime() -> None:
    with patch("custom_components.nodeping_status.sensor.dt_util") as mock_dt_util:
        mock_dt_util.now.return_value = datetime(2025, 1, 15, tzinfo=UTC)
        sensor = _make_sensor("today")
        assert sensor.native_value == pytest.approx(99.9)


def test_today_uptime_missing() -> None:
    with patch("custom_components.nodeping_status.sensor.dt_util") as mock_dt_util:
        mock_dt_util.now.return_value = datetime(2000, 1, 1, tzinfo=UTC)
        sensor = _make_sensor("today")
    assert sensor.native_value is None


def test_30day_uptime() -> None:
    sensor = _make_sensor("total")
    assert sensor.native_value == pytest.approx(99.5)


def test_30day_uptime_missing() -> None:
    sensor = _make_sensor("total", uptime={})
    assert sensor.native_value is None
