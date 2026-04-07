from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform

from types import SimpleNamespace
from twisted.internet import asyncioreactor
from twisted.internet.error import ReactorAlreadyInstalledError

import logging
_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SWITCH, Platform.NOTIFY]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    try:
        asyncioreactor.install(hass.loop)
    except ReactorAlreadyInstalledError:
        pass

    from konnect.protocols import MAX_TCP_PORT
    args = SimpleNamespace(
        name=entry.data["name"],
        debug=False,
        discovery_port=MAX_TCP_PORT,
        service_port=MAX_TCP_PORT,
        admin_port='/tmp/kde_connect.socket',
        config_dir=hass.config.path('kde_connect'),
        timestamps=True
    )

    from .server import start
    if not hasattr(entry, 'konnect'):
        entry.konnect = await hass.async_add_executor_job(start, hass, args)
        entry.konnect.location_name = hass.config.location_name

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    return unload_ok
