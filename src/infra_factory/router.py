"""Constraint-first model routing with explicit unit economics."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ModelCandidate:
    model_id: str
    provider: str
    capabilities: tuple[str, ...]
    input_usd_per_million: float
    output_usd_per_million: float
    p95_latency_ms: int
    reliability: float
    residency: str
    available: bool = True


@dataclass(frozen=True)
class RouteRequest:
    required_capabilities: tuple[str, ...]
    input_tokens: int
    output_tokens: int
    max_latency_ms: int
    minimum_reliability: float
    residency: str


def route_model(candidates: list[ModelCandidate], request: RouteRequest) -> dict:
    feasible = []
    rejected = []
    required = set(request.required_capabilities)
    for candidate in candidates:
        reasons = []
        if not candidate.available:
            reasons.append("unavailable")
        if not required.issubset(candidate.capabilities):
            reasons.append("capability")
        if candidate.p95_latency_ms > request.max_latency_ms:
            reasons.append("latency")
        if candidate.reliability < request.minimum_reliability:
            reasons.append("reliability")
        if request.residency != "any" and candidate.residency not in (request.residency, "local"):
            reasons.append("residency")
        cost = (
            request.input_tokens * candidate.input_usd_per_million
            + request.output_tokens * candidate.output_usd_per_million
        ) / 1_000_000
        if reasons:
            rejected.append({"model_id": candidate.model_id, "reasons": reasons})
        else:
            feasible.append((cost, candidate.p95_latency_ms, -candidate.reliability, candidate))
    if not feasible:
        return {"status": "no-feasible-model", "selected": None, "rejected": rejected}
    cost, _, _, selected = min(feasible)
    return {
        "status": "routed",
        "selected": {**asdict(selected), "estimated_cost_usd": round(cost, 6)},
        "rejected": rejected,
    }
