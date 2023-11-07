"""Adds config flow for CCEI Tild."""
import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import CONF_HOST, CONF_REFRESH_RATE, CONF_REFRESH_RATE_DEFAULT, DOMAIN
from .tild import CceiTildClient

LOGGER = logging.getLogger(__name__)


class CceiTildBaseConfigFlowHandler:
    """Base config flow for CCEI Tild."""

    async def check_tild_connection(self, host):
        """Test to connect on Tild box to validate new configuration"""
        try:
            client = CceiTildClient(host=host)
            state = await client.get_sensors_data()
            if not isinstance(state, dict):
                self._errors["base"] = "invalid_tild_data"
        except (OSError, ConnectionRefusedError):
            LOGGER.exception("Fail to connect on Tild host %s", host)
            self._errors["base"] = "connection_failed"

    def check_refresh_rate(self, value):
        """Check a given refresh_rate"""
        if not isinstance(value, int) or value <= 0:
            self._errors["base"] = "invalid_refresh_rate"

    async def check_user_input(self, user_input):
        """Check user config input"""
        self._errors = {}
        self.check_refresh_rate(user_input[CONF_REFRESH_RATE])
        if not self._errors:
            await self.check_tild_connection(user_input[CONF_HOST])

    @staticmethod
    def _get_config_schema(defaults=None):
        """Get configuration schema"""
        if not defaults:
            defaults = {CONF_REFRESH_RATE: CONF_REFRESH_RATE_DEFAULT}
        LOGGER.debug("defaults=%s", defaults)
        return vol.Schema(
            {
                vol.Required(CONF_HOST, default=defaults.get(CONF_HOST)): str,
                vol.Required(CONF_REFRESH_RATE, default=defaults.get(CONF_REFRESH_RATE)): int,
            }
        )


class CceiTildFlowHandler(CceiTildBaseConfigFlowHandler, config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for CCEI Tild."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            await self.check_user_input(user_input)
            if not self._errors:
                return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)

        return self.async_show_form(step_id="user", data_schema=self._get_config_schema(user_input))

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return CceiTildOptionsFlowHandler(config_entry)


class CceiTildOptionsFlowHandler(CceiTildBaseConfigFlowHandler, config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        self._errors = {}

        if user_input is not None:
            await self.check_user_input(user_input)
            if not self._errors:
                # update config entry
                self.hass.config_entries.async_update_entry(
                    self.config_entry, data=user_input, options=self.config_entry.options
                )
                return self.async_create_entry(title=self.config_entry.title, data=user_input)

        LOGGER.debug("Config entry=%s", self.config_entry)
        LOGGER.debug("Config entry options=%s", self.config_entry.options)
        return self.async_show_form(
            step_id="init",
            data_schema=self._get_config_schema(self.config_entry.options),
            errors=self._errors,
        )
