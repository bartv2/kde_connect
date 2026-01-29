from __future__ import annotations

from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass
from homeassistant.core import HomeAssistant
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
    konnect = config_entry.konnect

    new_devices = []
    for device in konnect.getDevices().values():
        identifier = device['identifier']
        client = konnect.findClient(identifier)
        new_devices.append(TrustedSwitch(konnect, client))
    if new_devices:
        async_add_entities(new_devices, update_before_add=True)


class TrustedSwitch(SwitchEntity):

    _attr_has_entity_name = True
    _attr_device_class = SwitchDeviceClass.SWITCH
    
    def __init__(self, konnect, client) -> None:
        self._konnect = konnect
        self._client = client
        self._name = "Trusted"
        self._attr_unique_id = client.identifier + "_trusted"
        self._state = None


    @property
    def name(self) -> str:
        """Return the display name of this switch."""
        return self._name

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._client.identifier)},
        }

    @property
    def is_on(self) -> bool | None:
        """Return true if switch is on."""
        return self._state

    def turn_on(self, **kwargs: Any) -> None:
        self._client.sendPair()

    def turn_off(self, **kwargs: Any) -> None:
        self._konnect.database.unpairDevice(self._client.identifier)
        self._client.sendUnpair()


    def update(self) -> None:
        self._state = self._client.isTrusted()
