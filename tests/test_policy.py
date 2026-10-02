from clinic.eval import run
from clinic.ingest import EVALS_PATH, load_notes
from clinic.policy import audit_event, route_note


def test_eval_file_passes():
    assert run(EVALS_PATH) == 0


def test_missing_consent_does_not_echo_the_note():
    decision = route_note(load_notes(), "NT-12")
    assert decision.route == "blocked_consent"
    assert "Sore throat" not in decision.render()
    event = audit_event(decision)
    assert "text" not in event
    assert event["note_id"] == "NT-12"


def test_refill_stays_on_the_nurse_queue():
    decision = route_note(load_notes(), "NT-13")
    assert decision.route == "nurse_queue"
    assert "diagnos" in decision.render().lower()
