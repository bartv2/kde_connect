"""Platform for binary_sensor integration."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import logging

from . import DOMAIN
_LOGGER = logging.getLogger(__name__)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the binary_sensor platform."""
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return
    konnect = discovery_info['konnect']
    add_entities([ReachableSensor(konnect, device) for device in konnect.getDevices().values()])



class ReachableSensor(BinarySensorEntity):

    _attr_has_entity_name = True
    _attr_device_class = BinarySensorDeviceClass.PRESENCE
    
    def __init__(self, konnect, device) -> None:
        """Initialize the sensor."""
        self._konnect = konnect
        self._device = device
        self._name = device['name']
        self._attr_unique_id = device['identifier']
        self._state = None


    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        _LOGGER.warning('Devices', self._konnect)
        return {
            "identifiers": {(DOMAIN, self._konnect.identifier)},
            # "name": self._konnect.name,
            # "sw_version": "1.0",
            # "model": "K",
            # "manufacturer": "KDE",
        }


    def update(self) -> None:
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._device['reachable']
