"""DataUpdateCoordinator for NodePing."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_URL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class NodePingCoordinator(DataUpdateCoordinator[dict]):
    """Coordinator to fetch NodePing status data."""

    def __init__(self, hass: HomeAssistant, report_id: str) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="NodePing",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.report_id = report_id

    async def _async_update_data(self) -> dict:
        """Fetch data from NodePing API."""
        session = async_get_clientsession(self.hass)
        url = API_URL.format(report_id=self.report_id)

        try:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise UpdateFailed(
                        f"Error fetching report {self.report_id}: HTTP {resp.status}"
                    )
                data = await resp.json()
        except UpdateFailed:
            raise
        except Exception as err:
            raise UpdateFailed(
                f"Error fetching report {self.report_id}: {err}"
            ) from err

        jobs: dict = {}
        for job in data.get("jobs", []):
            jobs[job["_id"]] = job

        return jobs
