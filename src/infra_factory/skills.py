"""Evidence-gated skill lifecycle; successful anecdotes cannot self-promote."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SkillCandidate:
    name: str
    version: str
    source_run_ids: tuple[str, ...]
    independent_eval_passes: int
    safety_regressions: int
    performance_delta: float


def promotion_decision(candidate: SkillCandidate, minimum_independent_passes: int = 3) -> dict:
    checks = {
        "multiple_source_runs": len(set(candidate.source_run_ids)) >= 2,
        "independent_evals": candidate.independent_eval_passes >= minimum_independent_passes,
        "no_safety_regression": candidate.safety_regressions == 0,
        "measurable_improvement": candidate.performance_delta > 0,
    }
    return {
        "skill": candidate.name,
        "version": candidate.version,
        "decision": "promote" if all(checks.values()) else "quarantine",
        "checks": checks,
    }
