# Northshore after-hours intake

<!-- project-guide:start -->
## Project guide

[Project architecture](PROJECT_ARCHITECTURE.md) · [Interview questions and answers](INTERVIEW_QA.md)

Use the architecture document for the component diagram, implementation boundaries, and verification entry points. The interview guide includes source-backed answers and project walkthroughs.

### Implementation map

| Component | Responsibility |
| --- | --- |
| [`src/clinic/policy.py`](src/clinic/policy.py) | Functions: `sentences`, `_urgent_sentence`, `route_note`, `audit_event`, `render` |
| [`src/clinic/eval.py`](src/clinic/eval.py) | Functions: `run` |
| [`src/clinic/ingest.py`](src/clinic/ingest.py) | Functions: `load_notes`, `load_cases` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`src/clinic/__init__.py`](src/clinic/__init__.py) | Implementation or supporting configuration |
| [`src/clinic/__main__.py`](src/clinic/__main__.py) | Functions: `main` |
| [`Dockerfile`](Dockerfile) | Container build/service configuration |
| [`tests/test_policy.py`](tests/test_policy.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |
| [`docs/01-discovery.md`](docs/01-discovery.md) | Project explanations or operating notes |
| [`docs/02-security.md`](docs/02-security.md) | Project explanations or operating notes |

### Local setup and verification

From the repository root (the commands follow the checked-in manifests):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

<!-- project-guide:end -->

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
