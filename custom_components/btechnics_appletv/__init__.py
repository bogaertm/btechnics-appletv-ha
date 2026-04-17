"""Btechnics Apple TV Radio - Home Assistant Integration."""
import logging
import os
import shutil

from homeassistant.core import HomeAssistant
from homeassistant.config import async_hass_config_yaml

_LOGGER = logging.getLogger(__name__)

DOMAIN = "btechnics_appletv"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
      """Set up the Btechnics Apple TV Radio integration."""
      # Copy the packages yaml to the HA packages directory
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
