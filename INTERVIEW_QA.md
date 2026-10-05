# fde-clinic-intake — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does fde-clinic-intake address, and what can you demonstrate?

Simulated forward deployed engagement for Northshore Clinic. The morning nurse was reading overnight portal notes in arrival order. Some had no consent. A few needed a callback before clinic opened. The clinic will not send note text to an outside model, and the tool must not diagnose.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/clinic/policy.py`](src/clinic/policy.py): Implementation or supporting configuration.
- [`src/clinic/eval.py`](src/clinic/eval.py): Implementation or supporting configuration.
- [`src/clinic/ingest.py`](src/clinic/ingest.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`src/clinic/__init__.py`](src/clinic/__init__.py): Implementation or supporting configuration.
- [`src/clinic/__main__.py`](src/clinic/__main__.py): Implementation or supporting configuration.
- [`Dockerfile`](Dockerfile): Container build/service configuration.
- [`tests/test_policy.py`](tests/test_policy.py): Executable checks and regression examples.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `route_note` and explain the decision it makes?

The main walkthrough here is `route_note(notes: dict[str, Note], note_id: str)` in [`src/clinic/policy.py`](src/clinic/policy.py#L55).

```python
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
```

This is an excerpt; follow the source link for the rest of the branches.

The implementation calls `Decision`, `NoteNotFound`, `_urgent_sentence`, `note.consent.strip`, `note.consent.strip().lower`. In an interview, trace those calls in execution order using a fixture input.

## 4. What responsibility does `run` have?

`run(path: Path | None=None)` is defined in [`src/clinic/eval.py`](src/clinic/eval.py#L9).

Its return expressions include:

- `0`
- `1`

It uses `case.get`, `decision.render`, `failures.append`, `len`, `load_cases`, `load_notes`, `print`, `route_note`. This is the code path I would compare against the caller to explain responsibility boundaries.

## 5. What input validation and failure behavior are implemented?

Explicit failure paths include:

- `SystemExit(main())` in [`src/clinic/__main__.py`](src/clinic/__main__.py#L25).
- `NoteNotFound(note_id)` in [`src/clinic/policy.py`](src/clinic/policy.py#L59).
- `RuntimeError(f'decision text must not contain {word}')` in [`src/clinic/policy.py`](src/clinic/policy.py#L39).

I would test both the condition that reaches each exception and the caller that translates it. An explicit raise does not mean every malformed input or dependency failure is handled.

## 6. Which test would you use to demonstrate correctness?

[`tests/test_policy.py`](tests/test_policy.py#L6) contains `test_eval_file_passes`:

```python
def test_eval_file_passes():
    assert run(EVALS_PATH) == 0
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 7. How do you separate the current design from a future production design?

The current design is the source/component map in [PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md). A future deployment needs explicit input contracts, persistence decisions, authentication, monitoring, and rollback. I would present these as proposed work until the corresponding implementation and verification exist.

## 8. Where does state live, and what happens with multiple workers?

Module-level containers include `URGENT_WORDS` in [`src/clinic/policy.py`](src/clinic/policy.py).

These containers belong to a Python process. Inspect which are constant fixtures and which are mutated. Mutable process state needs an explicit shared-storage or synchronization strategy before multiple workers can provide consistent behavior.

## 9. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 10. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 11. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 12. What is the input-to-output contract of `route_note`?

In [`src/clinic/policy.py`](src/clinic/policy.py#L55), `route_note(notes: dict[str, Note], note_id: str)` receives the inputs. The function computes these intermediate values:

- `citation = f'data/notes.csv#{note.note_id}'`
- `urgent = _urgent_sentence(note.text)`

Its result is defined by:

- `Decision(note_id=note.note_id, route='nurse_queue', reason='No urgent wording. Leave it on the morning nurse queue.', citation=citation)`
- `Decision(note_id=note.note_id, route='blocked_consent', reason='Consent is not yes, so the note body is not copied into the decision.', citation=citation)`
- `Decision(note_id=note.note_id, route='urgent_callback', reason=f'Call the on-call nurse before the morning queue. Trigger sentence: {urgent}', citation=f'{citation}#{urgent}')`

## 13. Which decision rules or boundary conditions should an interviewer challenge?

The implementation in [`src/clinic/policy.py`](src/clinic/policy.py#L55) branches on:

- `note.consent.strip().lower() != 'yes'`
- `urgent`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.
