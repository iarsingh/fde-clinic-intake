from __future__ import annotations

import re
from dataclasses import dataclass

URGENT_WORDS = {"chest", "breathing", "breath", "bleeding", "unresponsive", "fainted"}
FORBIDDEN = ("diagnosis", "diagnose", "prescribe", "dosage", "mg")


class NoteNotFound(KeyError):
    pass


@dataclass(frozen=True)
class Note:
    note_id: str
    patient_token: str
    consent: str
    text: str


@dataclass(frozen=True)
class Decision:
    note_id: str
    route: str
    reason: str
    citation: str

    def render(self) -> str:
        text = (
            f"Note {self.note_id} route: {self.route}.\n"
            f"{self.reason}\n"
            f"Citation: {self.citation}\n"
            "This is a queue decision for the on-call nurse. It is not a diagnosis.\n"
        )
        lowered = text.lower()
        for word in FORBIDDEN:
            if word in lowered and word not in "this is a queue decision for the on-call nurse. it is not a diagnosis.":
                raise RuntimeError(f"decision text must not contain {word}")
        return text


def sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]


def _urgent_sentence(text: str) -> str | None:
    for sentence in sentences(text):
        words = set(re.findall(r"[a-z]+", sentence.lower()))
        if words & URGENT_WORDS:
            return sentence
    return None


def route_note(notes: dict[str, Note], note_id: str) -> Decision:
    try:
        note = notes[note_id]
    except KeyError as exc:
        raise NoteNotFound(note_id) from exc
    citation = f"data/notes.csv#{note.note_id}"
    if note.consent.strip().lower() != "yes":
        return Decision(
            note_id=note.note_id,
            route="blocked_consent",
            reason="Consent is not yes, so the note body is not copied into the decision.",
            citation=citation,
        )
    urgent = _urgent_sentence(note.text)
    if urgent:
        return Decision(
            note_id=note.note_id,
            route="urgent_callback",
            reason=f"Call the on-call nurse before the morning queue. Trigger sentence: {urgent}",
            citation=f"{citation}#{urgent}",
        )
    return Decision(
        note_id=note.note_id,
        route="nurse_queue",
        reason="No urgent wording. Leave it on the morning nurse queue.",
        citation=citation,
    )


def audit_event(decision: Decision) -> dict[str, object]:
    return {
        "note_id": decision.note_id,
        "route": decision.route,
        "citation_count": 1,
    }
