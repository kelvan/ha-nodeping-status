"""Binary sensor platform for NodePing."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import NodePingCoordinator
from .entity import NodePingEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up NodePing binary sensors."""
    coordinator: NodePingCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        NodePingBinarySensor(coordinator, check_id) for check_id in coordinator.data
    )


class NodePingBinarySensor(NodePingEntity, BinarySensorEntity):
    """Binary sensor for a NodePing check."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_name = "Status"

    def __init__(self, coordinator: NodePingCoordinator, check_id: str) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator, check_id)
        self._attr_unique_id = f"{check_id}_status"

    @property
    def is_on(self) -> bool | None:
        """Return true if the check is up."""
        status = self._check_data.get("status")
        if status is None:
            return None
        return status == "up"

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra attributes."""
        data = self._check_data
        attrs = {}
        if "type" in data:
            attrs["check_type"] = data["type"]
        if "lastmessage" in data:
            attrs["last_message"] = data["lastmessage"]
        if "rt" in data:
            attrs["response_time"] = data["rt"]
        return attrs
