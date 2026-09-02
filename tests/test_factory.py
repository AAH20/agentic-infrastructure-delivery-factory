import unittest
from infra_factory.factory import DeliveryFactory
from infra_factory.models import *
R=[Resource("net","vnet","n",10,"critical","eu"),Resource("app","service","a",20,"standard","eu",("net",))]
C=Change("c","launch",("app",),1000,500,100,"EU","apply")
class Tests(unittest.TestCase):
 def test_verified_loop_and_context(self):
  o=Observation(0,5,.9,0,0,1,.5);r=DeliveryFactory().analyze(R,C,o,{"approved":True,"verification_passed":True,"engineering_hours_saved":2,"hourly_cost_usd":100,"inference_cost_usd":1,"test_cost_usd":2,"execution_cost_usd":3})
  self.assertEqual(r["payload"]["loop"]["status"],"verified");self.assertEqual(r["payload"]["bounded_context"],["app","net"])
 def test_policy_violation_blocks_apply(self):
  o=Observation(0,0,.5,0,1,.8,.5);r=DeliveryFactory().analyze(R,C,o,{"approved":True,"verification_passed":True,"engineering_hours_saved":0,"hourly_cost_usd":1,"inference_cost_usd":1,"test_cost_usd":1,"execution_cost_usd":1})
  self.assertEqual(r["payload"]["loop"]["status"],"blocked");self.assertEqual(r["payload"]["economics"]["verified_value_usd"],0)
 def test_verification_failure_rolls_back(self):
  o=Observation(0,0,1,0,0,1,.5);r=DeliveryFactory().analyze(R,C,o,{"approved":True,"verification_passed":False,"engineering_hours_saved":0,"hourly_cost_usd":1,"inference_cost_usd":1,"test_cost_usd":1,"execution_cost_usd":1})
  self.assertEqual(r["payload"]["loop"]["status"],"rolled-back")
if __name__=="__main__":unittest.main()

