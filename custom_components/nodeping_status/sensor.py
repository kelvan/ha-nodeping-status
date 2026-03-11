from __future__ import annotations

from datetime import date

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import NodePingCoordinator
from .entity import NodePingEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: NodePingCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = []
    for check_id in coordinator.data:
        entities.append(NodePingUptimeSensor(coordinator, check_id, "today"))
        entities.append(NodePingUptimeSensor(coordinator, check_id, "total"))
    async_add_entities(entities)


class NodePingUptimeSensor(NodePingEntity, SensorEntity):
    _attr_native_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 3

    def __init__(
        self, coordinator: NodePingCoordinator, check_id: str, period: str
    ) -> None:
        super().__init__(coordinator, check_id)
        self._period = period
        self._attr_unique_id = f"{check_id}_uptime_{period}"
        self._attr_name = "Today's Uptime" if period == "today" else "30-Day Uptime"

    @property
    def native_value(self) -> float | None:
        uptime = self._check_data.get("uptime", {})
        if self._period == "today":
            today_key = date.today().strftime("%Y-%m-%d")
            day_data = uptime.get(today_key, {})
            return day_data.get("uptime")
        # total / 30-day
        total_data = uptime.get("total", {})
        return total_data.get("uptime")
