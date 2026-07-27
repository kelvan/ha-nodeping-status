from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import NodePingConfigEntry, NodePingCoordinator
from .entity import NodePingEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: NodePingConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data

    async_add_entities(
        NodePingBinarySensor(coordinator, check_id) for check_id in coordinator.data
    )


class NodePingBinarySensor(NodePingEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_name = "Status"

    def __init__(self, coordinator: NodePingCoordinator, check_id: str) -> None:
        super().__init__(coordinator, check_id)
        self._attr_unique_id = f"{check_id}_status"

    @property
    def is_on(self) -> bool | None:
        status = self._check_data.get("status")
        if status is None:
            return None
        return status == "up"

    @property
    def extra_state_attributes(self) -> dict:
        data = self._check_data
        attrs = {}
        if "type" in data:
            attrs["check_type"] = data["type"]
        if "lastmessage" in data:
            attrs["last_message"] = data["lastmessage"]
        if "rt" in data:
            attrs["response_time"] = data["rt"]
        return attrs
