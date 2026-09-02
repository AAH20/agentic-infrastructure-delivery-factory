from dataclasses import dataclass,field
@dataclass(frozen=True)
class Resource:
 id:str;kind:str;owner:str;monthly_cost_usd:float;criticality:str;region:str;dependencies:tuple[str,...]=field(default_factory=tuple)
@dataclass(frozen=True)
class Change:
 id:str;goal:str;target_ids:tuple[str,...];estimated_revenue_usd:float;latency_slo_ms:int;budget_usd:float;residency:str;requested_action:str
@dataclass(frozen=True)
class Observation:
 prior_failures:int;similar_changes:int;test_coverage:float;plan_drift:int;policy_violations:int;dependency_coverage:float;capacity_utilization:float

