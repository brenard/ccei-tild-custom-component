"""Adds config flow for CCEI Tild."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import CONF_HOST, CONF_REFRESH_RATE, CONF_REFRESH_RATE_DEFAULT, DOMAIN


class CceiTildFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for CCEI Tild."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_REFRESH_RATE, default=CONF_REFRESH_RATE_DEFAULT): int,
                }
            ),
            errors=self._errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return CceiTildOptionsFlowHandler(config_entry)


class CceiTildOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            # update config entry
            self.hass.config_entries.async_update_entry(
                self.config_entry, data=user_input, options=self.config_entry.options
            )

            return self.async_create_entry(title=self.config_entry.title, data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST, default=self.config_entry.options.get(CONF_HOST)): str,
                    vol.Required(
                        CONF_REFRESH_RATE, default=self.config_entry.options.get(CONF_REFRESH_RATE)
                    ): int,
                }
            ),
        )
