"""Tests for the NodePing binary sensor."""

from unittest.mock import MagicMock

from custom_components.nodeping_status.binary_sensor import NodePingBinarySensor


def _make_sensor(data: dict) -> NodePingBinarySensor:
    coordinator = MagicMock()
    coordinator.data = data
    return NodePingBinarySensor(coordinator, "check001")


def test_status_up() -> None:
    sensor = _make_sensor({"check001": {"status": "up"}})
    assert sensor.is_on is True


def test_status_down() -> None:
    sensor = _make_sensor({"check001": {"status": "down"}})
    assert sensor.is_on is False


def test_status_missing() -> None:
    sensor = _make_sensor({"check001": {}})
    assert sensor.is_on is None


def test_attributes_present() -> None:
    sensor = _make_sensor(
        {
            "check001": {
                "status": "up",
                "type": "HTTPADV",
                "lastmessage": "Connection accepted",
                "rt": 145,
            }
        }
    )
    attrs = sensor.extra_state_attributes
    assert attrs["check_type"] == "HTTPADV"
    assert attrs["last_message"] == "Connection accepted"
    assert attrs["response_time"] == 145


def test_attributes_missing_optional() -> None:
    """Fields absent from the API response are not included in attributes."""
    sensor = _make_sensor({"check001": {"status": "down", "type": "HTTP"}})
    attrs = sensor.extra_state_attributes
    assert "response_time" not in attrs
    assert "last_message" not in attrs
