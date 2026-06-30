"""Config flow for AlertSwiss — pick the cantons that should alert you."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import CANTONS, CONF_CANTONS, CONF_INCLUDE_NATIONWIDE, DOMAIN


def _schema(defaults: dict) -> vol.Schema:
    return vol.Schema(
        {
            vol.Optional(CONF_CANTONS, default=defaults.get(CONF_CANTONS, [])): SelectSelector(
                SelectSelectorConfig(
                    options=CANTONS,
                    multiple=True,
                    mode=SelectSelectorMode.DROPDOWN,
                    custom_value=False,
                    sort=True,
                )
            ),
            vol.Optional(
                CONF_INCLUDE_NATIONWIDE, default=defaults.get(CONF_INCLUDE_NATIONWIDE, True)
            ): bool,
        }
    )


class AlertSwissConfigFlow(ConfigFlow, domain=DOMAIN):
    """Choose which cantons trigger alerts. No selection = whole of Switzerland."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="AlertSwiss", data=user_input)
        return self.async_show_form(step_id="user", data_schema=_schema({}))

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return AlertSwissOptionsFlow()


class AlertSwissOptionsFlow(OptionsFlow):
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        merged = {**self.config_entry.data, **self.config_entry.options}
        return self.async_show_form(step_id="init", data_schema=_schema(merged))
