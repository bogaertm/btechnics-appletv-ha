# Btechnics Apple TV Radio - Home Assistant Integratie

Home Assistant configuratie voor de Btechnics Apple TV Radio app. Hiermee bedien je de radio-app en camerafeed op je Apple TV rechtstreeks vanuit Home Assistant.

## Wat kan het?

**Radiobediening:** wissel van zender via een dropdown in je HA dashboard. Ondersteunt alle 12 zenders (VRT hoofdzenders, StuBru webradio's, Willy en TOPradio).

**Camera popup:** toon een RTSP camerastream als overlay op de Apple TV. Handig voor deurbellen, beveiligingscamera's of babyfoons. De radiostream blijft gewoon doorlopen (camera speelt zonder geluid).

## Installatie via HACS

1. Open HACS in Home Assistant
2. Ga naar het menu (drie puntjes rechtsboven) en kies **Aangepaste repositories**
3. Voeg toe: `https://github.com/bogaertm/btechnics-appletv-ha`
4. Kies categorie: **Integration**
5. Klik op **Toevoegen**
6. Zoek "Btechnics Apple TV Radio" en installeer
7. Herstart Home Assistant

### Packages activeren

Zorg dat packages ingeschakeld zijn in je `configuration.yaml`:

```yaml
homeassistant:
  packages: !include_dir_named packages
```

## Entiteiten

Na installatie en herstart zijn deze entiteiten beschikbaar:

| Entiteit | Type | Functie |
|---|---|---|
| `select.apple_tv_radio_magazijn` | Dropdown | Zender kiezen |
| `text.apple_tv_camera_url` | Tekstveld | RTSP URL van de camera |
| `number.apple_tv_camera_duur` | Schuifregelaar | Duur van de popup (10-300s) |
| `button.apple_tv_camera_tonen` | Knop | Camera popup openen |
| `button.apple_tv_camera_sluiten` | Knop | Camera popup sluiten |

## Gebruik

1. Voeg de entiteiten toe aan je dashboard
2. Kies een zender via de dropdown
3. Voor camera: vul de RTSP URL in, stel de duur in, druk op "Tonen"

## Vereisten

- Home Assistant met MQTT integratie (Mosquitto broker)
- Btechnics Apple TV Radio app op je Apple TV
- Apple TV en HA op hetzelfde netwerk

## MQTT Topics

| Topic | Richting | Functie |
|---|---|---|
| `btechnics/appletv/station/set` | HA → App | Zender instellen |
| `btechnics/appletv/station/state` | App → HA | Huidige zender |
| `btechnics/appletv/available` | App → HA | Online/offline status |
| `btechnics/appletv/camera/url/set` | HA → App | Camera URL instellen |
| `btechnics/appletv/camera/duration/set` | HA → App | Duur instellen |
| `btechnics/appletv/camera/show` | HA → App | Camera popup tonen |
| `btechnics/appletv/camera/hide` | HA → App | Camera popup sluiten |

## Licentie

MIT - Btechnics Elektriciteitswerken
