# Btechnics Play · Home Assistant integratie

Home Assistant koppeling voor **Btechnics Play** (vroeger Btechnics Apple TV Radio), de tvOS app van Btechnics op de Apple TV. Hiermee bedien je vanuit Home Assistant de radio, het volume, de lichtkrant en de live camerapopups op de Apple TV, en volg je de status van de stream op.

App versie: **Btechnics Play 1.4.0**

## Hoe het werkt

De app praat met Home Assistant via MQTT (Mosquitto broker). Alle topics beginnen met `btechnics/appletv`.

Er zijn twee soorten entiteiten:

1. **Entiteiten die de app zelf aanmaakt** via MQTT discovery. Die verschijnen vanzelf onder MQTT als het toestel **Btechnics Apple TV**, zodra de app draait.
2. **Entiteiten van deze integratie** (`btechnics_appletv`, via HACS): de zenderkeuze en de live camera's 1 tot 4.

## Installatie via HACS

1. Open HACS (in nieuwere Home Assistant versies: Marketplace).
2. Kies in het menu rechtsboven **Aangepaste repositories** en voeg `https://github.com/bogaertm/btechnics-appletv-ha` toe als **Integration**.
3. Installeer "Btechnics Apple TV Radio" en herstart Home Assistant.
4. Voeg de integratie toe via Instellingen, Apparaten en diensten.

Vereist: de MQTT integratie met een Mosquitto broker, en de Apple TV op hetzelfde netwerk. De app verbindt met de broker als gebruiker `AppleTV`.

## Entiteiten via MQTT discovery (toestel "Btechnics Apple TV")

De beschikbaarheid van alle entiteiten komt van `btechnics/appletv/available` (`online` of `offline`, retained, met Last Will).

| Entiteit | Type | Topic(s) | Functie |
|---|---|---|---|
| Nu speelt | sensor | `btechnics/appletv/nowplaying/state`, attributen uit `btechnics/appletv/nowplaying` (JSON: artist, title, show, presenter, station, cover) | Artiest en titel van wat er speelt |
| Show | sensor | `btechnics/appletv/nowplaying` (veld show) | Naam van het programma |
| Hoes | image | `btechnics/appletv/nowplaying/cover` | Hoes van het huidige nummer |
| Volume | number | `btechnics/appletv/volume/state` en `/set` (0 tot 100) | Volume van de app |
| Geluid uit | switch | `btechnics/appletv/mute/state` en `/set` (ON of OFF) | Geluid uit of aan |
| Afspelen | switch | `btechnics/appletv/playback/state` en `/set` (ON of OFF) | Afspelen of pauzeren |
| Lichtkrant melding | text | `btechnics/appletv/ticker/set` en `/state` (max 255 tekens) | Tekst die als lichtkrant over het beeld loopt |
| Stream status | sensor | `btechnics/appletv/stream/state` (JSON) | Status van de stream, zie hieronder |

### Stream status

Het bericht op `btechnics/appletv/stream/state` is JSON:

```json
{"status": "speelt", "fout": "", "zender": "Studio Brussel", "sinds": "2026-11-20T11:39:44Z"}
```

De sensor toont `status`. De velden `fout`, `zender` en `sinds` staan als attributen.

| Status | Betekenis |
|---|---|
| speelt | Alles werkt |
| hapert | De stream buffert of valt kort weg |
| ligt stil | De stream speelt niet meer |
| enkel geluid | De video viel weg, de app speelt tijdelijk de radiostream van dezelfde zender |
| geen internet | De Apple TV heeft geen internet |
| gepauzeerd | Bewust gepauzeerd |

## Entiteiten van de integratie (toestel "Btechnics Apple TV Radio")

| Entiteit | Type | Functie |
|---|---|---|
| `select.btechnics_apple_tv_radio_radio_magazijn` | select | Zender kiezen (`App niet ingeschakeld` als de app offline is) |
| `text.btechnics_apple_tv_radio_live_url_1` tot `_4` | text | URL van live camera 1 tot 4 (HLS of RTSP) |
| `number.btechnics_apple_tv_radio_live_duur` | number | Duur van een camerapopup (10 tot 300 s) |
| `button.btechnics_apple_tv_radio_live_url_1_tonen` tot `_4_tonen` | button | Camera 1 tot 4 tonen |
| `button.btechnics_apple_tv_radio_live_url_sluiten` | button | Camerapopup sluiten |

Zenders: Studio Brussel, MNM, Radio 1, Radio 2, Klara, De Tijdloze, UNTZ, Jaren Nul, Vuurland, Zware Gitaren, Willy en TOPradio. De namen in de select blijven zo; de app vertaalt Jaren Nul en TOPradio zelf naar de juiste stream.

## Live camera's met naam

Een camerapopup start je met een bericht op `btechnics/appletv/live/show1` tot `show4`. Dat mag nog altijd gewoon `ON` zijn (de app gebruikt dan de URL van dat kanaal en de ingestelde duur). Sinds 1.4.0 mag het ook JSON zijn, met een naam:

```json
{"url": "http://192.168.1.185:5000/api/go2rtc/api/stream.m3u8?src=Oprit&mp4", "duration": 45, "name": "Oprit"}
```

### Camerabeeld uit Frigate

De URL's van live camera 1 tot 4 komen rechtstreeks uit Frigate (go2rtc), via de interne Frigate poort 5000:

```
http://192.168.1.185:5000/api/go2rtc/api/stream.m3u8?src=<camera>&mp4
```

Zet altijd `&mp4` achter de URL. Zonder die optie levert go2rtc HLS in MPEG-TS, en daarin zitten geen beelden van H.265 camera's. Met `&mp4` wordt het fragmented MP4, het formaat dat een Apple TV nodig heeft voor H.265.

| Kanaal | Camera in Frigate |
|---|---|
| 1 | Oprit |
| 2 | Oprit_algemeen |
| 3 | Poort_LPR |
| 4 | VTO_Magazijn |

Het script `script.btechnics_play_camera` in Home Assistant stuurt de popup met de juiste naam (velden `nummer`, optioneel `naam` en `duur`).

De app toont dan "LIVE · CAMERA 1" met de naam als titel. Sluiten doe je met `btechnics/appletv/live/hide`.

Voorbeeld in Home Assistant:

```yaml
action: mqtt.publish
data:
  topic: btechnics/appletv/live/show1
  payload: >-
    {{ {'url': states('text.btechnics_apple_tv_radio_live_url_1'),
        'duration': 45, 'name': 'Oprit'} | to_json }}
```

## Alle MQTT topics

| Topic | Richting | Functie |
|---|---|---|
| `btechnics/appletv/available` | App → HA | online of offline (retained, Last Will) |
| `btechnics/appletv/station/set` | HA → App | Zender kiezen, of "Spotify" (sinds integratie 1.2.4): de app maakt Btechnics Play het actieve Spotify Connect toestel en hervat Spotify |
| `btechnics/appletv/station/state` | App → HA | Huidige zender, of "Spotify" zolang de bron spotify is (retained) |
| `btechnics/appletv/bron/fout` | App → HA | JSON met bron en reden als Spotify niet start (niet retained) |
| `btechnics/appletv/nowplaying` | App → HA | JSON met artist, title, show, presenter, station, cover |
| `btechnics/appletv/nowplaying/state` | App → HA | Artiest en titel als tekst |
| `btechnics/appletv/nowplaying/cover` | App → HA | URL van de hoes |
| `btechnics/appletv/volume/set` en `/state` | beide | Volume 0 tot 100 |
| `btechnics/appletv/mute/set` en `/state` | beide | Geluid uit (ON of OFF) |
| `btechnics/appletv/playback/set` en `/state` | beide | Afspelen (ON of OFF) |
| `btechnics/appletv/ticker/set` en `/state` | beide | Lichtkrant melding |
| `btechnics/appletv/stream/state` | App → HA | Stream status (JSON) |
| `btechnics/appletv/live/url1/set` tot `url4/set` en `/state` | beide | URL van live camera 1 tot 4 |
| `btechnics/appletv/camera/duration/set` en `/state` | beide | Duur van een camerapopup |
| `btechnics/appletv/live/show1` tot `show4` | HA → App | Camera tonen (`ON` of JSON met url, duration, name) |
| `btechnics/appletv/live/hide` | HA → App | Camerapopup sluiten |

## App heropenen vanuit Home Assistant

Is de app gesloten of gecrasht, dan kan Home Assistant ze opnieuw openen via de Apple TV integratie:

```yaml
action: media_player.select_source
target:
  entity_id: media_player.magazijn
data:
  source: Btechnics Play
```

Staat "Btechnics Play" niet in de bronnenlijst, herlaad dan de Apple TV integratie: de lijst met apps wordt enkel bij het verbinden opgehaald.

## Licentie

MIT, Btechnics Elektriciteitswerken
