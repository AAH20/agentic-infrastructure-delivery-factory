"""Authority-aware context selection under a hard token budget."""

from dataclasses import asdict, dataclass


AUTHORITY_WEIGHT = {"policy": 4, "desired-state": 3, "observed-state": 2, "retrieved": 1}


@dataclass(frozen=True)
class ContextItem:
    item_id: str
    authority: str
    relevance: float
    freshness: float
    token_count: int
    source: str
    content_digest: str
    contains_instructions: bool = False


def compile_context(items: list[ContextItem], token_budget: int) -> dict:
    """Select provenance-bearing context; retrieved instructions are data, never authority."""
    if token_budget < 1:
        raise ValueError("token_budget must be positive")
    rejected = []
    eligible = []
    for item in items:
        if item.authority not in AUTHORITY_WEIGHT:
            rejected.append({"item_id": item.item_id, "reason": "unknown-authority"})
        elif item.authority == "retrieved" and item.contains_instructions:
            rejected.append({"item_id": item.item_id, "reason": "untrusted-instructions"})
        else:
            score = AUTHORITY_WEIGHT[item.authority] * 10 + item.relevance * 5 + item.freshness
            eligible.append((score / max(item.token_count, 1), score, item))
    eligible.sort(key=lambda candidate: (candidate[0], candidate[1], candidate[2].item_id), reverse=True)
    selected = []
    used = 0
    for _, score, item in eligible:
        if used + item.token_count <= token_budget:
            selected.append({**asdict(item), "selection_score": round(score, 4)})
            used += item.token_count
        else:
            rejected.append({"item_id": item.item_id, "reason": "token-budget"})
    return {
        "token_budget": token_budget,
        "tokens_used": used,
        "selected": selected,
        "rejected": sorted(rejected, key=lambda entry: entry["item_id"]),
        "provenance_complete": all(item["source"] and item["content_digest"] for item in selected),
    }
