"""CCEI Tild update coordinator"""

from datetime import datetime, timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CLIENT, CONF_REFRESH_RATE_DEFAULT, DOMAIN, LAST_REFRESH, SENSORS_DATA


class CceiTildDataUpdateCoordinator(DataUpdateCoordinator):
    """CCEI Tild update coordinator"""

    def __init__(self, hass, logger, refresh_rate=None):
        super().__init__(
            hass,
            logger,
            name="CCEI Tild sensors data update",
            update_method=self._update_tild_data,
            update_interval=timedelta(
                minutes=refresh_rate if refresh_rate else CONF_REFRESH_RATE_DEFAULT
            ),
        )

    async def _update_tild_data(self):
        """Return the water consumption."""
        sensors_data = await self.hass.data[DOMAIN][CLIENT].get_sensors_data()
        return self._format_data(sensors_data)

    @staticmethod
    def _format_data(sensors_data):
        """Format coordinator data"""
        return {
            SENSORS_DATA: sensors_data,
            LAST_REFRESH: datetime.now().isoformat(),
        }

    def async_set_updated_sensors_data(self, sensors_data):
        """Manually update sensors data"""
        assert isinstance(sensors_data, dict), "Invalid sensors data provided, must be a dict."
        self.async_set_updated_data(self._format_data(sensors_data))

    def set_refresh_rate(self, refresh_rate):
        """Set refresh rate"""
        self.update_interval = timedelta(
            minutes=refresh_rate if refresh_rate else CONF_REFRESH_RATE_DEFAULT
        )
