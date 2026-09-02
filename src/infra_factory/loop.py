STAGES=("observe","retrieve-context","plan","validate","simulate","evaluate","approve","apply","verify","learn")
def execute_loop(*,policy_violations:int,approved:bool,verification_passed:bool)->dict[str,object]:
 completed=[]
 for stage in STAGES:
  if stage=="approve" and (policy_violations or not approved):return {"status":"blocked","blocked_at":"approve","completed":completed}
  if stage=="verify" and not verification_passed:return {"status":"rolled-back","blocked_at":"verify","completed":completed+["verify","rollback"]}
  completed.append(stage)
 return {"status":"verified","blocked_at":None,"completed":completed}

