"""AlertSwiss sensor: number of active alerts + details in attributes."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SEVERITY_ORDER

_SEV_NAME = {1: "minor", 2: "moderate", 3: "severe", 4: "extreme"}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, add: AddEntitiesCallback) -> None:
    add([AlertSwissSensor(hass.data[DOMAIN][entry.entry_id], entry)])


class AlertSwissSensor(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:alert-octagon"
    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = "Meldungen"

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_alerts"
        self._attr_name = "AlertSwiss Meldungen"

    @property
    def native_value(self) -> int:
        return len(self.coordinator.data.get("alerts", []))

    @property
    def extra_state_attributes(self) -> dict:
        alerts = self.coordinator.data.get("alerts", [])
        sev = max((SEVERITY_ORDER.get(a.get("severity"), 0) for a in alerts), default=0)
        return {
            "alerts": alerts,
            "titles": [a["title"] for a in alerts],
            "max_severity": _SEV_NAME.get(sev),
            "render_time": self.coordinator.data.get("render_time"),
        }
