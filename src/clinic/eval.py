from __future__ import annotations

from pathlib import Path

from clinic.ingest import load_cases, load_notes
from clinic.policy import route_note


def run(path: Path | None = None) -> int:
    notes = load_notes()
    failures = []
    cases = load_cases(path)
    for case in cases:
        decision = route_note(notes, case["note_id"])
        if decision.route != case["expected_route"]:
            failures.append(f"{case['note_id']}: {decision.route}")
        if case["expected_citation"] not in decision.citation:
            failures.append(f"{case['note_id']}: citation {decision.citation}")
        if case.get("body_forbidden") and case["body_forbidden"] in decision.render():
            failures.append(f"{case['note_id']}: echoed blocked text")
    if failures:
        print(f"{len(failures)} eval failure(s)")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"{len(cases)} eval cases passed")
    return 0
