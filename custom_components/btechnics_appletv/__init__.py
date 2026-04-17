"""Btechnics Apple TV Radio - Home Assistant Integration."""
import logging
import json

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components import mqtt

_LOGGER = logging.getLogger(__name__)

DOMAIN = "btechnics_appletv"

MQTT_ENTITIES = [
    {
        "component": "select",
        "object_id": "radio_magazijn",
        "config": {
            "name": "Apple TV Radio Magazijn",
            "unique_id": "btechnics_appletv_radio_magazijn",
            "command_topic": "btechnics/appletv/station/set",
            "state_topic": "btechnics/appletv/station/state",
            "availability_topic": "btechnics/appletv/available",
            "options": [
                "Studio Brussel",
                "MNM",
                "Radio 1",
                "Radio 2",
                "Klara",
                "De Tijdloze",
                "UNTZ",
                "Jaren Nul",
                "Vuurland",
                "Zware Gitaren",
                "Willy",
                "TOPradio"
            ],
            "icon": "mdi:radio",
        },
    },
    {
        "component": "text",
        "object_id": "camera_url",
        "config": {
            "name": "Apple TV Camera URL",
            "unique_id": "btechnics_appletv_camera_url",
            "command_topic": "btechnics/appletv/camera/url/set",
            "state_topic": "btechnics/appletv/camera/url/state",
            "availability_topic": "btechnics/appletv/available",
            "icon": "mdi:cctv",
        },
    },
    {
        "component": "number",
        "object_id": "camera_duration",
        "config": {
            "name": "Apple TV Camera Duur",
            "unique_id": "btechnics_appletv_camera_duration",
            "command_topic": "btechnics/appletv/camera/duration/set",
            "state_topic": "btechnics/appletv/camera/duration/state",
            "availability_topic": "btechnics/appletv/available",
            "min": 10,
            "max": 300,
            "step": 10,
            "unit_of_measurement": "s",
            "icon": "mdi:timer-outline",
        },
    },
    {
        "component": "button",
        "object_id": "camera_show",
        "config": {
            "name": "Apple TV Camera Tonen",
            "unique_id": "btechnics_appletv_camera_show",
            "command_topic": "btechnics/appletv/camera/show",
            "availability_topic": "btechnics/appletv/available",
            "icon": "mdi:cctv",
        },
    },
    {
        "component": "button",
        "object_id": "camera_hide",
        "config": {
            "name": "Apple TV Camera Sluiten",
            "unique_id": "btechnics_appletv_camera_hide",
            "command_topic": "btechnics/appletv/camera/hide",
            "availability_topic": "btechnics/appletv/available",
            "icon": "mdi:close-circle",
        },
    },
]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up via YAML (legacy)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Btechnics Apple TV Radio from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    for entity in MQTT_ENTITIES:
        topic = f"homeassistant/{entity['component']}/btechnics_appletv/{entity['object_id']}/config"
        payload = json.dumps(entity["config"])
        await mqtt.async_publish(hass, topic, payload, retain=True)
        _LOGGER.info("MQTT discovery gepubliceerd: %s", topic)

    _LOGGER.info("Btechnics Apple TV Radio integration geladen met %d entiteiten", len(MQTT_ENTITIES))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    for entity in MQTT_ENTITIES:
        topic = f"homeassistant/{entity['component']}/btechnics_appletv/{entity['object_id']}/config"
        await mqtt.async_publish(hass, topic, "", retain=True)

    hass.data.pop(DOMAIN, None)
    _LOGGER.info("Btechnics Apple TV Radio integration verwijderd")
    return True
