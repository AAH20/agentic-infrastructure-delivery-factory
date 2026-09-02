from dataclasses import asdict
from .context import ContextGraph
from .science import predict_failure,prescribe
from .loop import execute_loop
from .economics import calculate
from .evidence import receipt
class DeliveryFactory:
 def analyze(self,resources,change,observation,execution):
  context=ContextGraph(resources).bounded_context(change.target_ids)
  prediction=predict_failure(observation);actions=prescribe(observation,prediction["failure_probability"])
  loop=execute_loop(policy_violations=observation.policy_violations,approved=execution["approved"],verification_passed=execution["verification_passed"])
  economics=calculate(change.estimated_revenue_usd,execution["engineering_hours_saved"],execution["hourly_cost_usd"],execution["inference_cost_usd"],execution["test_cost_usd"],execution["execution_cost_usd"],loop["status"]=="verified")
  return receipt({"change":asdict(change),"bounded_context":context,"context_resources":len(context),"prediction":prediction,"prescriptions":actions,"loop":loop,"economics":economics,"kpis":{"dependency_coverage":observation.dependency_coverage,"test_coverage":observation.test_coverage,"capacity_utilization":observation.capacity_utilization},"evidence_tiers":{"engine":"implemented","case":"simulated","frameworks":"contract","nim":"contract","cloud":"contract"}})
