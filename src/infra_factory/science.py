from .models import Observation
def predict_failure(o:Observation)->dict[str,float|str]:
 z=-2.5+o.prior_failures*.45+o.plan_drift*.35+o.policy_violations*.7+(1-o.test_coverage)*2+(1-o.dependency_coverage)*2+max(0,o.capacity_utilization-.75)*3
 risk=1/(1+2.718281828**(-z));band="critical" if risk>=.75 else "high" if risk>=.5 else "medium" if risk>=.25 else "low"
 return {"failure_probability":round(risk,4),"risk_band":band,"model":"declared-logistic-reference-v1"}
def prescribe(o:Observation,risk:float)->list[str]:
 actions=[]
 if o.dependency_coverage<.9:actions.append("expand-dependency-discovery")
 if o.test_coverage<.85:actions.append("generate-and-run-regression-tests")
 if o.plan_drift:actions.append("refresh-state-and-replan")
 if o.policy_violations:actions.append("remediate-policy-before-approval")
 if o.capacity_utilization>.8:actions.append("reserve-or-scale-capacity")
 if risk>=.5:actions.append("canary-with-automatic-rollback")
 return actions or ["proceed-to-reviewed-plan"]

