"""Text platform for Btechnics Apple TV Radio."""
import logging

from homeassistant.components import mqtt
from homeassistant.components.text import TextEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    MQTT_AVAILABILITY,
    MQTT_CAMERA_URL_SET,
    MQTT_CAMERA_URL_STATE,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up text entities."""
    async_add_entities([BtechnicsCameraURL(entry)])


class BtechnicsCameraURL(TextEntity):
    """Camera URL input for Apple TV."""

    _attr_has_entity_name = True
    _attr_name = "Camera URL"
    _attr_icon = "mdi:cctv"
    _attr_native_value = None

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the text entity."""
        self._attr_unique_id = f"{DOMAIN}_camera_url"
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
            self._attr_native_value = msg.payload
            self.async_write_ha_state()

        @callback
        def availability_received(msg):
            """Handle availability updates."""
            self._available = msg.payload.lower() in ("online", "true", "1")
            self.async_write_ha_state()

        await mqtt.async_subscribe(self.hass, MQTT_CAMERA_URL_STATE, state_received)
        await mqtt.async_subscribe(self.hass, MQTT_AVAILABILITY, availability_received)

    async def async_set_value(self, value: str) -> None:
        """Set camera URL via MQTT."""
        await mqtt.async_publish(self.hass, MQTT_CAMERA_URL_SET, value)
        self._attr_native_value = value
        self.async_write_ha_state()
