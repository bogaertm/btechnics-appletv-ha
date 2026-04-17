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
    MQTT_LIVE_SHOW,
    MQTT_LIVE_HIDE,
)


_LOGGER = logging.getLogger(__name__)




async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up button entities."""
    entities = [BtechnicsLiveShowButton(entry, i) for i in range(4)]
    entities.append(BtechnicsLiveHideButton(entry))
    async_add_entities(entities)




class BtechnicsLiveShowButton(ButtonEntity):
    """Live stream show button for Apple TV."""


    _attr_has_entity_name = True
    _attr_icon = "mdi:cctv"


    def __init__(self, entry: ConfigEntry, index: int) -> None:
        """Initialize the button entity."""
        self._index = index
        self._num = index + 1
        self._entry = entry
        self._available = False
        self._attr_name = f"Live URL {self._num} Tonen"
        self._attr_unique_id = f"{DOMAIN}_live_show{self._num}"


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


        await mqtt.async_subscribe(
            self.hass, MQTT_AVAILABILITY, availability_received
        )


    async def async_press(self) -> None:
        """Handle button press."""
        await mqtt.async_publish(
            self.hass, MQTT_LIVE_SHOW[self._index], "ON"
        )




class BtechnicsLiveHideButton(ButtonEntity):
    """Live stream hide button for Apple TV."""


    _attr_has_entity_name = True
    _attr_name = "Live URL Sluiten"
    _attr_icon = "mdi:close-circle"


    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the button entity."""
        self._attr_unique_id = f"{DOMAIN}_live_hide"
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
        """Subscribe to availability topic."""
        @callback
        def availability_received(msg):
            """Handle availability updates."""
            self._available = msg.payload.lower() in ("online", "true", "1")
            self.async_write_ha_state()


        await mqtt.async_subscribe(
            self.hass, MQTT_AVAILABILITY, availability_received
        )


    async def async_press(self) -> None:
        """Handle button press."""
        await mqtt.async_publish(self.hass, MQTT_LIVE_HIDE, "ON")
