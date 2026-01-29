from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.discovery import load_platform
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform

from types import SimpleNamespace
from twisted.internet import asyncioreactor
from twisted.internet.error import ReactorAlreadyInstalledError

from .const import DOMAIN
import logging
_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SWITCH]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    try:
        asyncioreactor.install(hass.loop)
    except ReactorAlreadyInstalledError:
        pass

    from konnect.protocols import MAX_TCP_PORT
    args = SimpleNamespace(name=entry.data["name"], debug=True, discovery_port=MAX_TCP_PORT, service_port=MAX_TCP_PORT, admin_port="8080", config_dir="/tmp/konnect", timestamps=True)
    from .server import start
    if not hasattr(entry, 'konnect'):
        entry.konnect = await hass.async_add_executor_job(start, hass, args)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    return unload_ok
