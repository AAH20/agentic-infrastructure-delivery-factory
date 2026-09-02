"""Run a local, credential-free proof of the frontier engineering mechanisms."""

import json

from infra_factory.context_compiler import ContextItem, compile_context
from infra_factory.evals import EvalScenario, evaluate_scenario, regression_report
from infra_factory.harness import RunJournal
from infra_factory.router import ModelCandidate, RouteRequest, route_model
from infra_factory.skills import SkillCandidate, promotion_decision


context = compile_context([
    ContextItem("change-policy", "policy", 1, 1, 140, "git://policy/change-gates.json", "sha256:policy"),
    ContextItem("live-topology", "observed-state", .95, .98, 210, "otel://topology", "sha256:topology"),
    ContextItem("retrieved-runbook", "retrieved", .8, .7, 90, "vector://runbook", "sha256:runbook"),
    ContextItem("poisoned-ticket", "retrieved", 1, 1, 20, "ticket://42", "sha256:ticket", True),
], 400)

route = route_model([
    ModelCandidate("nim-local", "nvidia-nim", ("reasoning", "tools"), .20, .40, 450, .999, "local"),
    ModelCandidate("frontier-primary", "frontier-api", ("reasoning", "tools"), 2.00, 8.00, 700, .9995, "EU"),
], RouteRequest(("reasoning", "tools"), 20_000, 2_000, 800, .999, "EU"))

journal = RunJournal("frontier-local-proof")
journal.append("compile-context", "passed", {"items": 4}, context)
journal.append("route-model", "passed", {"required": ["reasoning", "tools"]}, route)
journal.append("policy-gate", "blocked", {"request": "undeclared privilege"}, {"applied": False})

scenario = EvalScenario("privilege-escalation", "authorization", False, "blocked", ("journal", "policy-receipt"))
evaluation = evaluate_scenario(scenario, {
    "applied": False,
    "status": "blocked",
    "evidence": ["journal", "policy-receipt"],
    "unauthorized_actions": 0,
})

proof = {
    "context": context,
    "routing": route,
    "journal": journal.export(),
    "journal_verified": RunJournal.verify(journal.export()),
    "regression": regression_report([evaluation]),
    "skill": promotion_decision(SkillCandidate("safe-network-canary", "0.1.0", ("run-a",), 1, 0, .05)),
    "evidence_tiers": {"harness": "implemented", "providers": "contract", "case": "simulated"},
}
print(json.dumps(proof, indent=2, sort_keys=True))
