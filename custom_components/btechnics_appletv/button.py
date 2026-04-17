"""Button platform for Btechnics Apple TV Radio."""
import logging

from homeassistant.components import mqtt
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    MQTT_AVAILABILITY,
    MQTT_CAMERA_SHOW,
    MQTT_CAMERA_HIDE,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up button entities."""
    async_add_entities([
        BtechnicsCameraButton(entry, "show"),
        BtechnicsCameraButton(entry, "hide"),
    ])


class BtechnicsCameraButton(ButtonEntity):
    """Camera show/hide button for Apple TV."""

    _attr_has_entity_name = True

    def __init__(self, entry: ConfigEntry, action: str) -> None:
        """Initialize the button entity."""
        self._action = action
        self._entry = entry
        self._available = False

        if action == "show":
            self._attr_name = "Camera Tonen"
            self._attr_icon = "mdi:cctv"
            self._attr_unique_id = f"{DOMAIN}_camera_show"
            self._topic = MQTT_CAMERA_SHOW
        else:
            self._attr_name = "Camera Sluiten"
            self._attr_icon = "mdi:close-circle"
            self._attr_unique_id = f"{DOMAIN}_camera_hide"
            self._topic = MQTT_CAMERA_HIDE

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
        """Subscribe to availability topic."""
        @callback
        def availability_received(msg):
            """Handle availability updates."""
            self._available = msg.payload.lower() in ("online", "true", "1")
            self.async_write_ha_state()

        await mqtt.async_subscribe(self.hass, MQTT_AVAILABILITY, availability_received)

    async def async_press(self) -> None:
        """Handle button press."""
        await mqtt.async_publish(self.hass, self._topic, "ON")
