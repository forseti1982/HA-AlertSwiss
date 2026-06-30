"""Constants for the AlertSwiss integration."""
from datetime import timedelta

DOMAIN = "alertswiss"

# Offizielle PolyAlert/AlertSwiss-Meldungen (BABS). Serverseitig abgerufen (kein CORS-Problem).
ALERTS_URL = (
    "https://www.alert.swiss/content/alertswiss-internet/de/home/"
    "_jcr_content/polyalert.alertswiss_alerts.actual.json"
)
USER_AGENT = "HomeAssistant-AlertSwiss/1.0 (+https://github.com/forseti1982/ha-alertswiss)"

SCAN_INTERVAL = timedelta(minutes=2)

CONF_KANTON = "kanton"          # optional: nur Meldungen mit passendem Kanton/Gebiet
CONF_INCLUDE_NATIONWIDE = "include_nationwide"

SEVERITY_ORDER = {"minor": 1, "moderate": 2, "severe": 3, "extreme": 4}
