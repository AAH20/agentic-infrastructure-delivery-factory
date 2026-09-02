from collections import deque
from .models import Resource
class ContextGraph:
 def __init__(self,resources:list[Resource]):
  self.items={x.id:x for x in resources};self.reverse={x.id:set() for x in resources}
  for x in resources:
   for d in x.dependencies:
    if d not in self.items:raise ValueError(f"missing dependency {d}")
    self.reverse[d].add(x.id)
 def bounded_context(self,targets:tuple[str,...],depth:int=2)->list[str]:
  seen=set(targets);q=deque((x,0) for x in targets)
  while q:
   node,level=q.popleft()
   if node not in self.items:raise ValueError(f"unknown target {node}")
   if level>=depth:continue
   for nxt in set(self.items[node].dependencies)|self.reverse[node]:
    if nxt not in seen:seen.add(nxt);q.append((nxt,level+1))
  return sorted(seen)

