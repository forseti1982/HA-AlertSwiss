"""The AlertSwiss integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    CONF_CANTONS,
    CONF_INCLUDE_NATIONWIDE,
    CONF_KANTON,
    CONF_LEVELS,
    DOMAIN,
)
from .coordinator import AlertSwissCoordinator

PLATFORMS = [Platform.BINARY_SENSOR, Platform.BUTTON, Platform.SENSOR]


def _cfg(entry: ConfigEntry, key, default):
    return entry.options.get(key, entry.data.get(key, default))


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    cantons = _cfg(entry, CONF_CANTONS, None)
    if not cantons:  # legacy single free-text -> list
        legacy = _cfg(entry, CONF_KANTON, "")
        cantons = [legacy] if legacy else []
    coordinator = AlertSwissCoordinator(
        hass,
        cantons=cantons,
        include_nationwide=_cfg(entry, CONF_INCLUDE_NATIONWIDE, True),
        levels=_cfg(entry, CONF_LEVELS, None),
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_reload))
    return True


async def _reload(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded
