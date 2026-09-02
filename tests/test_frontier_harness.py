import unittest

from infra_factory.context_compiler import ContextItem, compile_context
from infra_factory.evals import EvalScenario, evaluate_scenario, regression_report
from infra_factory.harness import RunJournal
from infra_factory.router import ModelCandidate, RouteRequest, route_model
from infra_factory.skills import SkillCandidate, promotion_decision


class FrontierHarnessTests(unittest.TestCase):
    def test_journal_verifies_and_detects_tampering(self):
        journal = RunJournal("run-1")
        journal.append("plan", "passed", {"goal": "scale"}, {"changes": 2})
        journal.append("verify", "passed", {"changes": 2}, {"slo": "met"})
        exported = journal.export()
        self.assertTrue(RunJournal.verify(exported))
        exported["events"][0]["status"] = "failed"
        self.assertFalse(RunJournal.verify(exported))

    def test_context_compiler_enforces_authority_and_budget(self):
        items = [
            ContextItem("policy", "policy", 1, 1, 40, "git://policy", "a"),
            ContextItem("state", "observed-state", .9, .9, 45, "otel://state", "b"),
            ContextItem("poison", "retrieved", 1, 1, 5, "vector://doc", "c", True),
        ]
        result = compile_context(items, 80)
        self.assertEqual([item["item_id"] for item in result["selected"]], ["policy"])
        self.assertIn({"item_id": "poison", "reason": "untrusted-instructions"}, result["rejected"])

    def test_router_selects_feasible_lowest_cost_model(self):
        candidates = [
            ModelCandidate("nim-local", "nvidia", ("tools",), .2, .4, 250, .999, "local"),
            ModelCandidate("cheap-unreliable", "other", ("tools",), .01, .01, 100, .8, "EU"),
        ]
        request = RouteRequest(("tools",), 10_000, 1_000, 500, .99, "EU")
        result = route_model(candidates, request)
        self.assertEqual(result["selected"]["model_id"], "nim-local")
        self.assertEqual(result["rejected"][0]["reasons"], ["reliability"])

    def test_eval_gate_and_skill_promotion(self):
        scenario = EvalScenario("policy-block", "policy", False, "blocked", ("policy-receipt",))
        result = evaluate_scenario(scenario, {
            "applied": False, "status": "blocked", "evidence": ["policy-receipt"], "unauthorized_actions": 0
        })
        self.assertEqual(regression_report([result])["release_gate"], "pass")
        candidate = SkillCandidate("safe-canary", "1.1.0", ("run-1", "run-2"), 3, 0, .12)
        self.assertEqual(promotion_decision(candidate)["decision"], "promote")


if __name__ == "__main__":
    unittest.main()
