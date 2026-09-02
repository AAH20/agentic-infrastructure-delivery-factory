# Frontier-grade agent engineering layer

This layer is designed around a harder question than “can an agent generate Terraform?”: **can an operator prove why a change was proposed, what authority it used, which model and tools were selected, what happened at every stage, and whether a learned behavior deserves promotion?**

## Implemented mechanisms

| Mechanism | Failure addressed | Verifiable output |
|---|---|---|
| Authority-aware context compiler | stale context, prompt injection and context-window overflow | selected/rejected items, provenance and token accounting |
| Constraint-first model router | model outage, residency breach, latency or cost overrun | feasibility reasons, chosen provider and estimated per-call cost |
| Tamper-evident run journal | irreproducible agent behavior and unverifiable claims | hash-chained stage events with independent verification |
| Adversarial evaluation harness | happy-path-only demos and silent regressions | scenario checks, score, failures and release decision |
| Evidence-gated skill promotion | self-modification from one anecdotal success | quarantine/promote decision with independent-eval threshold |

These modules have no network or cloud dependency and run in CI. Provider integration, NVIDIA NIM inference and infrastructure execution remain explicit contracts until configured and evidenced.

## Context authority

The compiler separates four types of context:

1. `policy`: immutable constraints and approval boundaries;
2. `desired-state`: version-controlled intent;
3. `observed-state`: current telemetry and inventory;
4. `retrieved`: useful but untrusted supporting material.

Retrieved content that contains instructions is rejected. This is deliberately stricter than asking a model to decide whether an instruction is trustworthy. Every selected item retains a source and digest.

## Durable replay

Each stage records digests of its inputs and outputs, the previous event hash and its own hash. A replay verifier detects reordered, missing or mutated events. Production adapters should add signed identities, timestamps from a trusted clock and an immutable evidence store; the local implementation proves the chain semantics, not those external controls.

## Model routing

Routing is a constraint problem before it is an optimization problem. Candidates that fail capability, availability, residency, reliability or latency constraints are rejected. Cost ranks only feasible candidates. This supports NVIDIA NIM, frontier APIs and local open-weight models through contracts without claiming equivalence between models.

## Learning without uncontrolled self-modification

A successful run may propose a skill candidate, but it cannot promote itself. Promotion requires multiple source runs, independent evaluation passes, no safety regression and measurable improvement. Failed candidates stay quarantined with their evidence.

## Production extension points

- Replace declared prices and reliability with measured provider telemetry.
- Sign journals using workload identity and anchor receipts in immutable storage.
- Execute IaC only inside disposable sandboxes with scoped credentials.
- Add shadow traffic, canaries, rollback drills and service-level verification.
- Maintain separate train, evaluation and incident-derived holdout suites.
- Report task success, intervention rate, unsafe action rate, cost, latency and verified business value together.

## Public engineering basis

- [OpenAI: Harness engineering](https://openai.com/index/harness-engineering/) emphasizes legible environments, enforceable invariants and feedback loops.
- [OpenAI: Trustworthy third-party evaluations](https://openai.com/index/trustworthy-third-party-evaluations-foundations/) treats harness, tools, budgets and validity checks as part of an evaluation claim.
- [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) frames context as a finite resource that must be curated across long-running loops.
- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) describes evaluations as a compounding mechanism for exposing regressions before production.
- [NVIDIA: NeMo Agent Toolkit evaluation](https://docs.nvidia.com/nemo/agent-toolkit/latest/workflows/evaluate.html) documents curated datasets, workflow artifacts, profiling and custom evaluators.
- [NVIDIA: NIM LLM API](https://docs.nvidia.com/nim/large-language-models/latest/function-calling.html) documents the OpenAI-compatible inference surface and operational health/metrics endpoints used by the provider contract.
