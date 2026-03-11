from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import NodePingCoordinator


class NodePingEntity(CoordinatorEntity[NodePingCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coordinator: NodePingCoordinator, check_id: str) -> None:
        super().__init__(coordinator)
        self._check_id = check_id

    @property
    def _check_data(self) -> dict:
        return self.coordinator.data.get(self._check_id, {})

    @property
    def device_info(self) -> DeviceInfo:
        data = self._check_data
        return DeviceInfo(
            identifiers={(DOMAIN, self._check_id)},
            name=data.get("label", self._check_id),
            manufacturer="NodePing",
            model=data.get("type"),
        )
