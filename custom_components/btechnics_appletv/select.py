"""Select platform for Btechnics Apple TV Radio."""
import logging

from homeassistant.components import mqtt
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    MQTT_AVAILABILITY,
    MQTT_STATION_SET,
    MQTT_STATION_STATE,
    RADIO_STATIONS,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up select entities."""
    async_add_entities([BtechnicsRadioSelect(entry)])


class BtechnicsRadioSelect(SelectEntity):
    """Radio station selector for Apple TV."""

    _attr_has_entity_name = True
    _attr_name = "Radio Magazijn"
    _attr_icon = "mdi:radio"
    _attr_options = RADIO_STATIONS
    _attr_current_option = None

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the select entity."""
        self._attr_unique_id = f"{DOMAIN}_radio_magazijn"
        self._entry = entry
        self._available = False

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._available

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, "appletv_radio")},
            "name": "Btechnics Apple TV Radio",
            "manufacturer": "Btechnics",
            "model": "Apple TV Radio App",
        }

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT topics."""
        @callback
        def state_received(msg):
            """Handle state updates."""
            value = msg.payload
            if value in self._attr_options:
                self._attr_current_option = value
                self.async_write_ha_state()

        @callback
        def availability_received(msg):
            """Handle availability updates."""
            self._available = msg.payload.lower() in ("online", "true", "1")
            self.async_write_ha_state()

        await mqtt.async_subscribe(self.hass, MQTT_STATION_STATE, state_received)
        await mqtt.async_subscribe(self.hass, MQTT_AVAILABILITY, availability_received)

    async def async_select_option(self, option: str) -> None:
        """Send selected station via MQTT."""
        await mqtt.async_publish(self.hass, MQTT_STATION_SET, option)
        self._attr_current_option = option
        self.async_write_ha_state()
