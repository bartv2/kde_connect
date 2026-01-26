"""
Configuration:

To use the kde_connect component you will need to add the following to your
configuration.yaml file.

kde_connect:
"""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.discovery import load_platform
from homeassistant.helpers.typing import ConfigType

from types import SimpleNamespace
from twisted.internet import asyncioreactor

DOMAIN = "kde_connect"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    # States are in the format DOMAIN.OBJECT_ID.
    hass.states.async_set('kde_connect.KC_Hello_World', 'Works 1!')
    asyncioreactor.install(hass.loop)
    from konnect.protocols import MAX_TCP_PORT
    args = SimpleNamespace(name="HomeAssistant", debug=True, discovery_port=MAX_TCP_PORT, service_port=MAX_TCP_PORT, admin_port="8080", config_dir="/tmp/konnect", timestamps=True)
    from .server import start
    konnect = await hass.async_add_executor_job(start, hass, args)
    load_platform(hass, 'binary_sensor', DOMAIN, {'konnect': konnect}, config)

    return True
