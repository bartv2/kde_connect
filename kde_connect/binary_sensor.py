"""Platform for binary_sensor integration."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN
from konnect import __version__ as konnect_version


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for passed config_entry in HA."""
    konnect = config_entry.konnect

    new_devices = []
    for device in konnect.getDevices().values():
        new_devices.append(ReachableSensor(konnect, device))
    if new_devices:
        async_add_entities(new_devices)


class ReachableSensor(BinarySensorEntity):

    _attr_has_entity_name = True
    _attr_device_class = BinarySensorDeviceClass.PRESENCE
    
    def __init__(self, konnect, device) -> None:
        """Initialize the sensor."""
        self._konnect = konnect
        self._device = device
        self._name = "Reachable"
        self._attr_unique_id = device['identifier'] + "_reachable"
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
        #_LOGGER.warning('Devices', self._konnect)
        return {
            "identifiers": {(DOMAIN, self._device['identifier'])},
            "name": self._device['name'],
            "sw_version": konnect_version,
            "model": self._device['type'],
            "manufacturer": "Konnect",
        }


    def update(self) -> None:
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._device['reachable']
