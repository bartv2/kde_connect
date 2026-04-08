from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from konnect.factories import KonnectFactory
from konnect.protocols import Konnect

from .const import DOMAIN
import logging
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    konnect = config_entry.konnect

    new_devices = []
    for device in konnect.getDevices().values():
        identifier = device['identifier']
        client = konnect.findClient(identifier)
        if client is None:
            continue
        new_devices.append(TrustedSwitch(konnect, client))
    if new_devices:
        async_add_entities(new_devices, update_before_add=True)


class TrustedSwitch(SwitchEntity):

    _attr_has_entity_name = True
    _attr_device_class = SwitchDeviceClass.SWITCH

    def __init__(self, konnect: KonnectFactory, client: Konnect) -> None:
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
