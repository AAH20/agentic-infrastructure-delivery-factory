"""Durable, tamper-evident execution journal for agent runs."""

from dataclasses import asdict, dataclass
from hashlib import sha256
import json


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class RunEvent:
    sequence: int
    stage: str
    status: str
    input_digest: str
    output_digest: str
    previous_hash: str
    event_hash: str


class RunJournal:
    """Append-only journal that can be independently replay-verified."""

    def __init__(self, run_id: str):
        self.run_id = run_id
        self.events: list[RunEvent] = []

    def append(self, stage: str, status: str, inputs: object, outputs: object) -> RunEvent:
        previous_hash = self.events[-1].event_hash if self.events else "GENESIS"
        core = {
            "run_id": self.run_id,
            "sequence": len(self.events),
            "stage": stage,
            "status": status,
            "input_digest": sha256(_canonical(inputs).encode()).hexdigest(),
            "output_digest": sha256(_canonical(outputs).encode()).hexdigest(),
            "previous_hash": previous_hash,
        }
        event_fields = {key: value for key, value in core.items() if key != "run_id"}
        event = RunEvent(**event_fields, event_hash=sha256(_canonical(core).encode()).hexdigest())
        self.events.append(event)
        return event

    def export(self) -> dict:
        return {"run_id": self.run_id, "events": [asdict(event) for event in self.events]}

    @staticmethod
    def verify(document: dict) -> bool:
        previous_hash = "GENESIS"
        for expected_sequence, event in enumerate(document.get("events", [])):
            if event.get("sequence") != expected_sequence or event.get("previous_hash") != previous_hash:
                return False
            core = {key: event[key] for key in (
                "sequence", "stage", "status", "input_digest", "output_digest", "previous_hash"
            )}
            core["run_id"] = document.get("run_id")
            if sha256(_canonical(core).encode()).hexdigest() != event.get("event_hash"):
                return False
            previous_hash = event["event_hash"]
        return bool(document.get("events"))
