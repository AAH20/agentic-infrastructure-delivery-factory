import hashlib,json
from datetime import datetime,timezone
def receipt(payload):
 e={"schema":"agentic.infrastructure.delivery.v1","evidence_class":"simulated","generated_at":datetime.now(timezone.utc).isoformat(),"payload":payload};e["sha256"]=hashlib.sha256(json.dumps(e,sort_keys=True,separators=(",",":")).encode()).hexdigest();e["integrity_note"]="Digest detects envelope changes; it does not prove deployment, model accuracy, identity or custody.";return e

