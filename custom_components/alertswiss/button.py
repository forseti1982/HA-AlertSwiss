"""AlertSwiss test button — manually trigger a test message (like the app's Push-Test)."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, add: AddEntitiesCallback) -> None:
    add([AlertSwissTestButton(hass.data[DOMAIN][entry.entry_id], entry)])


class AlertSwissTestButton(ButtonEntity):
    _attr_has_entity_name = True
    _attr_icon = "mdi:bell-ring"

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        self._coordinator = coordinator
        self._attr_unique_id = f"{entry.entry_id}_test"
        self._attr_name = "AlertSwiss Testmeldung"

    async def async_press(self) -> None:
        self._coordinator.inject_test()
