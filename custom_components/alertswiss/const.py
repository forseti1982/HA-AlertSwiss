"""Constants for the AlertSwiss integration."""
from datetime import timedelta

DOMAIN = "alertswiss"

ALERTS_URL = (
    "https://www.alert.swiss/content/alertswiss-internet/de/home/"
    "_jcr_content/polyalert.alertswiss_alerts.actual.json"
)
USER_AGENT = "HomeAssistant-AlertSwiss/1.1 (+https://github.com/forseti1982/HA-AlertSwiss)"

SCAN_INTERVAL = timedelta(minutes=2)

CONF_CANTONS = "cantons"
CONF_KANTON = "kanton"  # legacy (single free-text), kept for backward compatibility
CONF_INCLUDE_NATIONWIDE = "include_nationwide"
CONF_LEVELS = "levels"

# Meldestufen (UI) <- alert.swiss severity
LEVELS = ["Alarm", "Warnung", "Info"]
SEVERITY_TO_LEVEL = {
    "extreme": "Alarm",
    "severe": "Alarm",
    "moderate": "Warnung",
    "minor": "Info",
}

# 26 Schweizer Kantone (Namen wie auf alert.swiss / publisherName "Kanton …")
CANTONS = [
    "Zürich", "Bern", "Luzern", "Uri", "Schwyz", "Obwalden", "Nidwalden",
    "Glarus", "Zug", "Freiburg", "Solothurn", "Basel-Stadt", "Basel-Landschaft",
    "Schaffhausen", "Appenzell Ausserrhoden", "Appenzell Innerrhoden", "St. Gallen",
    "Graubünden", "Aargau", "Thurgau", "Tessin", "Waadt", "Wallis",
    "Neuenburg", "Genf", "Jura",
]

SEVERITY_ORDER = {"minor": 1, "moderate": 2, "severe": 3, "extreme": 4}
