"""Constants for Btechnics Apple TV Radio."""

DOMAIN = "btechnics_appletv"

# MQTT Topics
MQTT_BASE = "btechnics/appletv"
MQTT_AVAILABILITY = f"{MQTT_BASE}/available"

MQTT_STATION_SET = f"{MQTT_BASE}/station/set"
MQTT_STATION_STATE = f"{MQTT_BASE}/station/state"

# Live URL topics (4 streams)
MQTT_LIVE_URL_SET = [f"{MQTT_BASE}/live/url{i}/set" for i in range(1, 5)]
MQTT_LIVE_URL_STATE = [f"{MQTT_BASE}/live/url{i}/state" for i in range(1, 5)]

# Live show/hide topics
MQTT_LIVE_SHOW = [f"{MQTT_BASE}/live/show{i}" for i in range(1, 5)]
MQTT_LIVE_HIDE = f"{MQTT_BASE}/live/hide"

# Camera duur
MQTT_CAMERA_DURATION_SET = f"{MQTT_BASE}/camera/duration/set"
MQTT_CAMERA_DURATION_STATE = f"{MQTT_BASE}/camera/duration/state"

# Radio stations
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
