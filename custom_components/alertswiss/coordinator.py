"""DataUpdateCoordinator for AlertSwiss."""
from __future__ import annotations

import logging

import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import ALERTS_URL, SCAN_INTERVAL, SEVERITY_TO_LEVEL, USER_AGENT

_LOGGER = logging.getLogger(__name__)


def _clean(alert: dict) -> dict:
    """Reduce a raw PolyAlert entry to the fields we expose."""
    title = (alert.get("title") or {}).get("title") or alert.get("event") or "Meldung"
    desc = (alert.get("description") or {}).get("description") or ""
    instructions = [i.get("text") for i in (alert.get("instructions") or []) if i.get("text")]
    severity = alert.get("severity")
    return {
        "identifier": alert.get("identifier"),
        "title": title,
        "event": alert.get("event"),
        "severity": severity,
        "level": SEVERITY_TO_LEVEL.get(severity, "Info"),
        "publisher": alert.get("publisherName"),
        "sent": alert.get("sent"),
        "description": desc,
        "instructions": instructions,
        "nationwide": bool(alert.get("nationWide")),
        "link": alert.get("link"),
        "areas": alert.get("areas") or [],
    }


def _test_alert() -> dict:
    """A clearly-marked manual test message."""
    return {
        "identifier": "TEST",
        "title": "\U0001F9EA TEST – Probemeldung AlertSwiss",
        "event": "Test",
        "severity": "minor",
        "level": "Info",
        "publisher": "AlertSwiss (Test)",
        "sent": "jetzt",
        "description": "Manuell ausgelöste Testmeldung zur Prüfung Deiner Benachrichtigungen.",
        "instructions": ["Keine Aktion nötig – dies ist nur ein Test."],
        "nationwide": True,
        "link": None,
        "areas": [],
        "test": True,
    }


class AlertSwissCoordinator(DataUpdateCoordinator):
    """Fetches and filters AlertSwiss alerts."""

    def __init__(self, hass: HomeAssistant, cantons: list[str] | None = None,
                 include_nationwide: bool = True, levels: list[str] | None = None) -> None:
        super().__init__(hass, _LOGGER, name="AlertSwiss", update_interval=SCAN_INTERVAL)
        self._cantons = [c.strip().lower() for c in (cantons or []) if c and c.strip()]
        self._include_nationwide = include_nationwide
        self._levels = list(levels or [])  # empty = all levels

    def _level_ok(self, alert: dict) -> bool:
        return not self._levels or alert.get("level") in self._levels

    def inject_test(self) -> None:
        """Manually push a test alert so notifications/automations can be verified."""
        data = dict(self.data or {"alerts": [], "render_time": None})
        data["alerts"] = [_test_alert()] + list(data.get("alerts", []))
        self.hass.bus.async_fire("alertswiss_test", {"alert": _test_alert()})
        self.async_set_updated_data(data)

    def _matches(self, alert: dict) -> bool:
        # No cantons selected -> whole of Switzerland.
        if not self._cantons:
            return True
        if self._include_nationwide and alert.get("nationwide"):
            return True
        hay = " ".join(
            [str(alert.get("publisher") or "")]
            + [str(a) for a in (alert.get("areas") or [])]
        ).lower()
        return any(c in hay for c in self._cantons)

    async def _async_update_data(self):
        session = async_get_clientsession(self.hass)
        try:
            async with async_timeout.timeout(20):
                resp = await session.get(ALERTS_URL, headers={"User-Agent": USER_AGENT})
                resp.raise_for_status()
                raw = await resp.json(content_type=None)
        except Exception as err:  # noqa: BLE001
            raise UpdateFailed(f"AlertSwiss-Abruf fehlgeschlagen: {err}") from err

        alerts = []
        for a in raw.get("alerts", []) or []:
            if a.get("testAlert") or a.get("technicalTestAlert") or a.get("allClear"):
                continue
            ca = _clean(a)
            if self._matches(ca):
                alerts.append(ca)
        return {"alerts": alerts, "render_time": raw.get("renderTime")}
