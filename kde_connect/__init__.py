"""
Configuration:

To use the kde_connect component you will need to add the following to your
configuration.yaml file.

kde_connect:
"""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "kde_connect"


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up a skeleton component."""
    # States are in the format DOMAIN.OBJECT_ID.
    hass.states.set('kde_connect.KC_Hello_World', 'Works!')

    # Return boolean to indicate that initialization was successfully.
    return True
