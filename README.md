# 🇨🇭 AlertSwiss für Home Assistant

Offizielle Schweizer Behörden-Warnungen (**PolyAlert / BABS**, Quelle [alert.swiss](https://www.alert.swiss)) als Home-Assistant-Sensoren. Der Abruf erfolgt **serverseitig** (kein CORS-Problem), alle 2 Minuten.

## Entitäten
- `sensor.alertswiss_meldungen` – Anzahl aktiver Meldungen. Attribute: `alerts` (Titel, Ereignis, Schweregrad, Herausgeber, Beschreibung, Anweisungen, Link), `titles`, `max_severity`.
- `binary_sensor.alertswiss_warnung_aktiv` – `on`, sobald eine Warnung aktiv ist (device_class: safety).

## Installation (HACS)
1. HACS → ⋮ → **Benutzerdefinierte Repositories** → `https://github.com/forseti1982/ha-alertswiss` (Kategorie: Integration).
2. **AlertSwiss** installieren, Home Assistant neu starten.
3. Einstellungen → Geräte & Dienste → **Integration hinzufügen** → *AlertSwiss*. Optional einen Kanton/Gebiet-Filter angeben (z. B. `Zürich`).

## Beispiel-Automation (Push bei neuer Warnung)
```yaml
trigger:
  - platform: state
    entity_id: binary_sensor.alertswiss_warnung_aktiv
    to: "on"
action:
  - service: notify.notify
    data:
      title: "⚠️ AlertSwiss"
      message: "{{ state_attr('sensor.alertswiss_meldungen','titles') | join(', ') }}"
```

## Hinweis
Inoffizielle Integration. Test-/Übungsmeldungen und „Entwarnungen" werden herausgefiltert. Daten © BABS / alert.swiss.
