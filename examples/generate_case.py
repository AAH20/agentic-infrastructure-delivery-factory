import json
from pathlib import Path
resources=[]
for i in range(240):
 resources.append({"id":f"res-{i:03d}","kind":["vnet","cluster","service","database","gpu-pool","policy"][i%6],"owner":f"team-{i%12}","monthly_cost_usd":500+(i%20)*175,"criticality":"critical" if i<12 else "standard","region":["germany-west-central","west-europe","us-east","on-prem"][i%4],"dependencies":[] if i<12 else [f"res-{i%12:03d}"]})
case={"resources":resources,"change":{"id":"chg-eu-ai-support","goal":"launch EU-resident AI support at 5000 RPM","target_ids":["res-012","res-013","res-014"],"estimated_revenue_usd":180000,"latency_slo_ms":800,"budget_usd":45000,"residency":"EU","requested_action":"provision-and-connect"},"observation":{"prior_failures":1,"similar_changes":14,"test_coverage":.91,"plan_drift":0,"policy_violations":0,"dependency_coverage":.94,"capacity_utilization":.83},"execution":{"approved":True,"verification_passed":True,"engineering_hours_saved":120,"hourly_cost_usd":135,"inference_cost_usd":240,"test_cost_usd":850,"execution_cost_usd":2100}}
Path(__file__).with_name("synthetic-multicloud-change.json").write_text(json.dumps(case,indent=2)+"\n")
