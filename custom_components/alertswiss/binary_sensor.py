"""AlertSwiss binary sensor: any active alert."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, add: AddEntitiesCallback) -> None:
    add([AlertSwissActive(hass.data[DOMAIN][entry.entry_id], entry)])


class AlertSwissActive(CoordinatorEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.SAFETY
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_active"
        self._attr_name = "AlertSwiss Warnung aktiv"

    @property
    def is_on(self) -> bool:
        return len(self.coordinator.data.get("alerts", [])) > 0

    @property
    def extra_state_attributes(self) -> dict:
        alerts = self.coordinator.data.get("alerts", [])
        return {"count": len(alerts), "titles": [a["title"] for a in alerts]}
