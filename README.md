# Northshore after-hours intake

Simulated forward deployed engagement for Northshore Clinic. The morning nurse was reading overnight portal notes in arrival order. Some had no consent. A few needed a callback before clinic opened. The clinic will not send note text to an outside model, and the tool must not diagnose.

## What the nurse lead gets

A route, not a diagnosis.

| Note | Consent | Route |
| --- | --- | --- |
| NT-11 chest tightness | yes | urgent_callback, citing that sentence |
| NT-14 bleeding that will not stop | yes | urgent_callback |
| NT-13 refill request | yes | nurse_queue |
| NT-12 sore throat | no | blocked_consent, body not copied |

The audit event stores note id, route, and citation count. It does not store the note text.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
pytest
python -m clinic eval
python -m clinic NT-11
```

## Docs

- [Discovery](docs/01-discovery.md)
- [Security](docs/02-security.md)
- [Readout](docs/03-readout.md)

This does not claim fewer adverse events. The shadow-week number is: every note without consent stays blocked, and the nurse lead agrees with the route on at least 9 of 10 reviewed notes.
