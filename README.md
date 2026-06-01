# Leistungskurve_II

Dieses Projekt berechnet und visualisiert eine Leistungszeitkurve (Power Curve) auf Basis von Leistungswerten über die Zeit.

## Dateien

- `power_curve.py`: Enthält die Funktion `power_curve`, die aus einer Liste von Leistungsdaten die maximale durchschnittliche Leistung für verschiedene Zeitdauern berechnet und die Kurve darstellt.
- `main.py`: Projektstartpunkt oder Beispielskript.
- `activity.csv`: Datendatei mit Aktivitätsdaten (falls vorhanden).
- `pyproject.toml`: Projektkonfiguration und Abhängigkeiten.

## Anforderungen

- Python 3.9 oder neuer
- pandas
- numpy
- matplotlib

## Installation

1. Virtuelle Umgebung erstellen und aktivieren:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Abhängigkeiten installieren:

```powershell
pip install pandas numpy matplotlib
```

## Nutzung

Um die Leistungszeitkurve zu berechnen und anzuzeigen, starte das Skript oder importiere `power_curve`:

```powershell
python -c "from power_curve import power_curve; power_curve([100, 200, 150, 120], time_s=1)"
```

Alternativ kannst du `power_curve.py` direkt ausführen, wenn dort ein entsprechender Aufruf im `__main__`-Block hinterlegt ist.

## Funktion

Die Funktion `power_curve`:

- nimmt Leistungswerte (`power_data`) und eine Zeitauflösung (`time_s`) entgegen
- berechnet für verschiedene Zeitdauern den höchsten gleitenden Durchschnitt
- erstellt ein Diagramm mit Dauer auf der x-Achse und Leistung auf der y-Achse

## Lizenz

Projekt ohne spezifische Lizenzangabe. Bei Bedarf kannst du eine passende Lizenz ergänzen.
