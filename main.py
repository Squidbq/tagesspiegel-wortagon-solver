#!/usr/bin/env python3
# File: main.py

import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple


def load_data(file_path: Path) -> Dict[str, List[Dict]]:
    """Puzzle-Daten aus JSON laden."""
    try:
        with file_path.open(encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        sys.exit(f"Error: Datei nicht gefunden: {file_path}")
    except json.JSONDecodeError as e:
        sys.exit(f"Error: Ungültiges JSON: {e}")
    if not isinstance(data, dict):
        sys.exit("Error: Erwartetes Top-Level-Objekt ist kein Dict.")
    return data


def decode_ascii_pairs(code: str) -> str:
    """Zwei‑stellige ASCII-Codes zu Text umwandeln."""
    if len(code) % 2:
        raise ValueError(f"Ungültige Länge: {code!r}")
    try:
        return "".join(chr(int(code[i : i + 2])) for i in range(0, len(code), 2))
    except ValueError as e:
        raise ValueError(f"Ungültiger ASCII-Code in {code!r}: {e}")


def is_isogram(word: str) -> bool:
    """True, wenn kein Buchstabe doppelt vorkommt."""
    return len(set(word)) == len(word)


def score_word(word: str) -> int:
    """Punktevergabe: Isogramm=10, Länge 4=1, sonst=Len."""
    if is_isogram(word):
        return 10
    if len(word) == 4:
        return 1
    return len(word)


def choose_words(
    candidates: List[Tuple[str, int]], target: int = 80
) -> Tuple[List[Tuple[str, int]], int]:
    """Höchste Kandidaten aufsammeln, bis target erreicht ist."""
    total = 0
    chosen: List[Tuple[str, int]] = []
    for word, pts in sorted(candidates, key=lambda x: x[1], reverse=True):
        chosen.append((word, pts))
        total += pts
        if total >= target:
            break
    return chosen, total


def select_date(dates: List[str]) -> str:
    """Datumsauswahl: Gestern/Heute/Morgen oder aus Liste."""
    today = date.today()
    presets = {
        "1": ("Gestern", (today - timedelta(days=1)).isoformat()),
        "2": ("Heute", today.isoformat()),
        "3": ("Morgen", (today + timedelta(days=1)).isoformat()),
        "4": ("Aus Liste", None),
    }

    while True:
        print("Wähle Datum:")
        for key, (label, _) in presets.items():
            print(f"  {key}. {label}")
        choice = input("Eingabe [1-4]: ").strip()
        if choice in ("1", "2", "3"):
            return presets[choice][1]  # type: ignore
        if choice == "4":
            break
        print("Ungültig, bitte erneut.\n")

    sorted_dates = sorted(dates)
    print("\nVerfügbare Termine:")
    for idx, iso in enumerate(sorted_dates, 1):
        dt = datetime.fromisoformat(iso)
        print(f"  {idx}. {dt.day:02d}.{dt.month:02d}.{dt.year}")
    sel = input(f"Datum wählen [1-{len(sorted_dates)}]: ").strip()
    if sel.isdigit() and 1 <= (i := int(sel)) <= len(sorted_dates):
        return sorted_dates[i - 1]
    print("Ungültig, setze auf Gestern.")
    return presets["1"][1]  # type: ignore


def format_german(d: str) -> str:
    """ISO-Datum ↔ Deutsches Format TT.MM.JJJJ."""
    dt = datetime.fromisoformat(d)
    return f"{dt.day:02d}.{dt.month:02d}.{dt.year}"


def process_puzzle(p: Dict, date_iso: str) -> None:
    """Ein Puzzle dekodieren, auswerten und ausgeben."""
    nr = p.get("nr", "?")
    try:
        middle = decode_ascii_pairs(p["letter"]).lower()
        main_iso = decode_ascii_pairs(p["isogram"]).lower()
    except (KeyError, ValueError) as e:
        print(f"Puzzle #{nr}: Fehler, überspringe ({e})")
        return

    # Kandidaten sammeln
    candidates: List[Tuple[str, int]] = []
    for code in p.get("possibilities", []):
        try:
            w = decode_ascii_pairs(code).lower()
        except ValueError:
            continue
        if len(w) < 4 or middle not in w:
            continue
        candidates.append((w, score_word(w)))

    # Weitere Isogramme
    sorted_main = sorted(main_iso)
    extras = [
        w
        for w, _ in candidates
        if w != main_iso and len(w) == len(main_iso) and sorted(w) == sorted_main
    ]

    chosen, total = choose_words(candidates)

    hdr_date = format_german(date_iso)
    sep = "=" * 50
    print(f"\n{sep}\n Puzzle #{nr}    Datum: {hdr_date}\n{sep}\n")

    print(f"Haupt-Isogramm (10 Punkte): {main_iso}\n")

    print("Weitere Isogramme (je 10 Punkte):")
    print("  " + (", ".join(extras) if extras else "(keine)") + "\n")

    print(f"Auswahl für ≥80 Punkte: {total} Punkte mit {len(chosen)} Wörtern")
    max_len = max((len(w) for w, _ in chosen), default=0)
    for idx, (w, pts) in enumerate(chosen, 1):
        print(f"  {idx:2}. {w:<{max_len}} {pts} Punkte")
    print()


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: python main.py data.json")
    data = load_data(Path(sys.argv[1]))
    date_iso = select_date(list(data.keys()))
    puzzles = data.get(date_iso) or []
    if not puzzles:
        sys.exit(f"Keine Daten für {format_german(date_iso)}")
    for puzzle in puzzles:
        process_puzzle(puzzle, date_iso)


if __name__ == "__main__":
    main()