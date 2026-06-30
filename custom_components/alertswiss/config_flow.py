"""Config flow for AlertSwiss."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.core import callback

from .const import CONF_INCLUDE_NATIONWIDE, CONF_KANTON, DOMAIN


def _schema(defaults: dict) -> vol.Schema:
    return vol.Schema(
        {
            vol.Optional(CONF_KANTON, default=defaults.get(CONF_KANTON, "")): str,
            vol.Optional(
                CONF_INCLUDE_NATIONWIDE, default=defaults.get(CONF_INCLUDE_NATIONWIDE, True)
            ): bool,
        }
    )


class AlertSwissConfigFlow(ConfigFlow, domain=DOMAIN):
    """UI configuration: optional Kanton filter (e.g. 'Zürich')."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="AlertSwiss", data=user_input)
        return self.async_show_form(step_id="user", data_schema=_schema({}))

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return AlertSwissOptionsFlow(config_entry)


class AlertSwissOptionsFlow(OptionsFlow):
    def __init__(self, entry: ConfigEntry) -> None:
        self._entry = entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        merged = {**self._entry.data, **self._entry.options}
        return self.async_show_form(step_id="init", data_schema=_schema(merged))
