# Tagesspiegel Wortagon Solver

Ein Python-Skript zur Analyse und Lösung der täglichen Wort‑Puzzles von wortagon.tagesspiegel.de.

## Voraussetzungen

- Python 3.7 oder neuer (keine externen Bibliotheken)

## Installation

1. Repository klonen  
   ```bash
   git clone https://github.com/Squidbq/tagesspiegel-wortagon-solver.git
   cd tagesspiegel-wortagon-solver
   ```
2. (Optional) Virtuelle Umgebung anlegen  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

## Daten beschaffen

1. Browser öffnen unter  
   https://wortagon.tagesspiegel.de/  
2. Entwicklertools (F12) → Network → nach "get" filtern  
3. Anfrage `https://wortagon.tagesspiegel.de/api/get` auswählen  
4. Im Reiter **Response** den gesamten JSON-Inhalt kopieren  
5. In Datei `data.json` im Projektverzeichnis einfügen

## Verwendung

```bash
python main.py data.json
```

Das Skript fragt nach einem Datum (Gestern/Heute/Morgen/aus Liste) und liefert:

- Haupt‑Isogramm (10 Punkte)  
- Weitere Isogramme (je 10 Punkte)  
- Wortauswahl für ≥ 80 Punkte

## Datenformat

Datei `data.json`:
```json
{
  "YYYY-MM-DD": [
    {
      "nr": 123,
      "letter": "080105...",
      "isogram": "080105...",
      "possibilities": ["080105...", "..."]
    }
  ]
}
```

## Lizenz

MIT License
