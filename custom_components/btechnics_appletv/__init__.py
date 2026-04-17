"""Btechnics Apple TV Radio - Home Assistant Integration."""
import logging
import os
import shutil

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "btechnics_appletv"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
          """Set up via YAML (legacy)."""
          return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
          """Set up Btechnics Apple TV Radio from a config entry."""
          hass.data.setdefault(DOMAIN, {})

    # Copy packages yaml if not already present
          packages_dir = hass.config.path("packages")
          source = os.path.join(
              os.path.dirname(__file__), "..", "..", "packages", "btechnics_appletv.yaml"
          )
          dest = os.path.join(packages_dir, "btechnics_appletv.yaml")

    if os.path.exists(source) and not os.path.exists(dest):
                  os.makedirs(packages_dir, exist_ok=True)
                  shutil.copy2(source, dest)
                  _LOGGER.info("Btechnics Apple TV: package YAML gekopieerd naar %s", dest)

    _LOGGER.info("Btechnics Apple TV Radio integration geladen")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
          """Unload a config entry."""
          hass.data.pop(DOMAIN, None)
          return True
