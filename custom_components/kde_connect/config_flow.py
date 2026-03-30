from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN

DATA_SCHEMA = vol.Schema({vol.Required("name", default="HomeAssistant"): str})

class KDEConnectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    # MINOR_VERSION = 1

    async def async_step_user(self, user_input):
        if user_input is not None:
            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA
        )
