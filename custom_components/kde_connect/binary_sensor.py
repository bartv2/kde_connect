"""Platform for binary_sensor integration."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
import logging
_LOGGER = logging.getLogger(__name__)
from konnect import __version__ as konnect_version


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for passed config_entry in HA."""
    konnect = config_entry.konnect

    new_devices = []
    device_registry = dr.async_get(hass)
    for device in konnect.getDevices().values():
        identifier = device['identifier']
        device_registry.async_get_or_create(
            config_entry_id=config_entry.entry_id,
            identifiers={(DOMAIN, identifier)},
            name=device['name'],
            sw_version=konnect_version,
            model=device['type'],
            manufacturer="Konnect",
        )
        client = konnect.findClient(identifier)
        if client is None:
            continue
        new_devices.append(ReachableSensor(konnect, client))
    if new_devices:
        async_add_entities(new_devices, update_before_add=True)


class ReachableSensor(BinarySensorEntity):

    _attr_has_entity_name = True
    _attr_device_class = BinarySensorDeviceClass.PRESENCE
    
    def __init__(self, konnect, client) -> None:
        """Initialize the sensor."""
        self._konnect = konnect
        self._client = client
        self._name = "Reachable"
        self._attr_unique_id = client.identifier + "_reachable"
        self._state = None


    @property
    def name(self) -> str:
        """Return the display name of this sensor."""
        return self._name

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._client.identifier)},
        }

    @property
    def is_on(self) -> bool | None:
        """Return true if sensor is on."""
        return self._state


    def update(self) -> None:
        devices = self._konnect.getDevices()
        try:
            self._state = devices[self._client.identifier]['reachable']
        except KeyError:
            self._state = None
