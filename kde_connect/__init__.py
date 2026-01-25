"""
Configuration:

To use the kde_connect component you will need to add the following to your
configuration.yaml file.

kde_connect:
"""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

# from konnect.server import start
from types import SimpleNamespace
from twisted.internet import asyncioreactor

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "kde_connect"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    # States are in the format DOMAIN.OBJECT_ID.
    hass.states.async_set('kde_connect.KC_Hello_World', 'Works 1!')
    asyncioreactor.install(hass.loop)
    from konnect.protocols import MAX_TCP_PORT
    args = SimpleNamespace(name="HomeAssistant", debug=True, discovery_port=MAX_TCP_PORT, service_port=MAX_TCP_PORT, admin_port="8080", config_dir="/tmp/konnect", timestamps=True)
    from .server import start
    site=await hass.async_add_executor_job(start, hass, args)
    # await hass.loop.create_server(site, host="127.0.0.1", port=8081)
    hass.states.async_set('kde_connect.KC_Hello_World', 'Works 2!')

    # Return boolean to indicate that initialization was successfully.
    return True
