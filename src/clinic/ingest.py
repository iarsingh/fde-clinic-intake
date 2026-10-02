from __future__ import annotations

import csv
import json
from pathlib import Path

from clinic.policy import Note

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
EVALS_PATH = ROOT / "evals" / "questions.jsonl"


def load_notes(path: Path | None = None) -> dict[str, Note]:
    notes: dict[str, Note] = {}
    with (path or DATA_DIR / "notes.csv").open(newline="") as handle:
        for row in csv.DictReader(handle):
            note = Note(
                note_id=row["note_id"],
                patient_token=row["patient_token"],
                consent=row["consent"],
                text=row["text"],
            )
            notes[note.note_id] = note
    return notes


def load_cases(path: Path | None = None) -> list[dict]:
    cases = []
    for line in (path or EVALS_PATH).read_text().splitlines():
        if line.strip():
            cases.append(json.loads(line))
    return cases
