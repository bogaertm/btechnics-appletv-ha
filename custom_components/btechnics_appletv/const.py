"""Constants for Btechnics Apple TV Radio."""

DOMAIN = "btechnics_appletv"

# MQTT Topics
MQTT_BASE = "btechnics/appletv"
MQTT_AVAILABILITY = f"{MQTT_BASE}/available"

MQTT_STATION_SET = f"{MQTT_BASE}/station/set"
MQTT_STATION_STATE = f"{MQTT_BASE}/station/state"

MQTT_CAMERA_URL_SET = f"{MQTT_BASE}/camera/url/set"
MQTT_CAMERA_URL_STATE = f"{MQTT_BASE}/camera/url/state"

MQTT_CAMERA_DURATION_SET = f"{MQTT_BASE}/camera/duration/set"
MQTT_CAMERA_DURATION_STATE = f"{MQTT_BASE}/camera/duration/state"

MQTT_CAMERA_SHOW = f"{MQTT_BASE}/camera/show"
MQTT_CAMERA_HIDE = f"{MQTT_BASE}/camera/hide"

RADIO_STATIONS = [
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
    "TOPradio",
]
