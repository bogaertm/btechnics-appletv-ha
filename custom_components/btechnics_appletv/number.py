"""Number platform for Btechnics Apple TV Radio."""
import logging

from homeassistant.components import mqtt
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    MQTT_AVAILABILITY,
    MQTT_CAMERA_DURATION_SET,
    MQTT_CAMERA_DURATION_STATE,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up number entities."""
    async_add_entities([BtechnicsCameraDuration(entry)])


class BtechnicsCameraDuration(NumberEntity):
    """Camera popup duration for Apple TV."""

    _attr_has_entity_name = True
    _attr_name = "Camera Duur"
    _attr_icon = "mdi:timer-outline"
    _attr_native_min_value = 10
    _attr_native_max_value = 300
    _attr_native_step = 10
    _attr_native_unit_of_measurement = "s"
    _attr_native_value = None

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the number entity."""
        self._attr_unique_id = f"{DOMAIN}_camera_duration"
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
            try:
                self._attr_native_value = float(msg.payload)
                self.async_write_ha_state()
            except (ValueError, TypeError):
                _LOGGER.warning("Ongeldige waarde voor camera duur: %s", msg.payload)

        @callback
        def availability_received(msg):
            """Handle availability updates."""
            self._available = msg.payload.lower() in ("online", "true", "1")
            self.async_write_ha_state()

        await mqtt.async_subscribe(self.hass, MQTT_CAMERA_DURATION_STATE, state_received)
        await mqtt.async_subscribe(self.hass, MQTT_AVAILABILITY, availability_received)

    async def async_set_native_value(self, value: float) -> None:
        """Set camera duration via MQTT."""
        await mqtt.async_publish(self.hass, MQTT_CAMERA_DURATION_SET, str(int(value)))
        self._attr_native_value = value
        self.async_write_ha_state()
