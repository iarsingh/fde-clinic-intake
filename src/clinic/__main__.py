from __future__ import annotations

import sys

from clinic.eval import run
from clinic.ingest import load_notes
from clinic.policy import NoteNotFound, audit_event, route_note


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "eval":
        return run()
    note_id = sys.argv[1] if len(sys.argv) > 1 else "NT-11"
    try:
        decision = route_note(load_notes(), note_id)
    except NoteNotFound:
        print(f"Unknown note {note_id}", file=sys.stderr)
        return 1
    print(decision.render())
    print(audit_event(decision))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
