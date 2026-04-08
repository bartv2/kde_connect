from __future__ import annotations

from homeassistant.components.notify import NotifyEntity, NotifyEntityFeature
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
        new_devices.append(DeviceNotify(konnect, client))
    if new_devices:
        async_add_entities(new_devices, update_before_add=True)


class DeviceNotify(NotifyEntity):

    _attr_has_entity_name = True

    def __init__(self, konnect: KonnectFactory, client: Konnect) -> None:
        self._konnect = konnect
        self._client = client
        self._name = "Notifier"
        self._attr_unique_id = client.identifier + "_notify"
        self._attr_supported_features = NotifyEntityFeature.TITLE

    @property
    def name(self) -> str:
        """Return the display name of this notify."""
        return self._name

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._client.identifier)},
        }

    def send_message(self, message: str, title: str | None = None) -> None:
        """Send a message."""
        self._client.sendNotification(message, title, self._konnect.location_name, None)
