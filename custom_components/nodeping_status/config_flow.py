from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_NAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import API_URL, CONF_REPORT_ID, DOMAIN


class NodePingConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            report_id = user_input[CONF_REPORT_ID].strip()
            name = user_input[CONF_NAME].strip()

            if not report_id:
                errors[CONF_REPORT_ID] = "no_report_id"
            elif not name:
                errors[CONF_NAME] = "no_name"
            else:
                self._async_abort_entries_match({CONF_REPORT_ID: report_id})

                try:
                    session = async_get_clientsession(self.hass)
                    async with session.get(API_URL.format(report_id=report_id)) as resp:
                        if resp.status == 404:
                            errors[CONF_REPORT_ID] = "invalid_report_id"
                        elif resp.status != 200:
                            errors["base"] = "cannot_connect"
                except Exception:
                    errors["base"] = "cannot_connect"

                if not errors:
                    return self.async_create_entry(
                        title=name,
                        data={CONF_REPORT_ID: report_id},
                    )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_REPORT_ID): str,
                    vol.Required(CONF_NAME): str,
                }
            ),
            errors=errors,
        )
