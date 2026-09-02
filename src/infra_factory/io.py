import json
from pathlib import Path
from .models import Resource,Change,Observation
def load(path):
 d=json.loads(Path(path).read_text());rs=[]
 for x in d["resources"]:y=dict(x);y["dependencies"]=tuple(y.get("dependencies",[]));rs.append(Resource(**y))
 c=dict(d["change"]);c["target_ids"]=tuple(c["target_ids"])
 return rs,Change(**c),Observation(**d["observation"]),d["execution"]

