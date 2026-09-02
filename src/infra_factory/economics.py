def calculate(revenue:float,engineering_hours_saved:float,hourly_cost:float,inference:float,test_cost:float,execution:float,verified:bool)->dict[str,float|None]:
 cost=inference+test_cost+execution;labor=engineering_hours_saved*hourly_cost;value=revenue+labor if verified else 0;net=value-cost
 return {"verified_value_usd":round(value,2),"delivery_cost_usd":round(cost,2),"net_value_usd":round(net,2),"cost_per_verified_change_usd":round(cost,2) if verified else None,"roi":round(net/cost,4) if cost else None}

