# Wasserstands-Monitoring Agger (Station 2728759000100)

Dieses System dient der automatisierten Überwachung und Dokumentation des Wasserstands der Agger. Es stellt sicher, dass kritische Pegelstände frühzeitig erkannt und für spätere Analysen rechtzeitig archiviert werden.

### Kernfunktionen

* **Automatisierte Datenerfassung:** Der Pegelstand wird stündlich direkt vom Hochwasserportal NRW abgerufen.
* **Digitale Pegel-Historie:** Alle Messwerte werden fortlaufend in einer CSV-Datei (`agger_wasserstand.csv`) protokolliert – ideal für Digitalisierung und Visualisierung.
* **Frühwarnsystem:** Bei Überschreitung eines definierten Schwellenwerts (**250,0 cm**) erfolgt eine sofortige Benachrichtigung via Push-Alarm (ntfy).

### Technische Eckpunkte

* **Intervall:** Stündliche Abfrage.
* **Datenquelle:** Offizielle JSON-Schnittstelle des Hochwasserportals NRW.
* **System:** Cloud-basiertes Skript (GitHub Actions), wartungsfrei und ohne eigenen Serverbetrieb.

### Nutzen für das Büro

Die Anwendung ersetzt das manuelle Prüfen von Pegelwebseiten und bietet eine lückenlose Datengrundlage zur Beurteilung der lokalen Hochwasserlage oder für hydrologische Fragestellungen im Projektgebiet.
