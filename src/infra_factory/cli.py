import argparse,json
from pathlib import Path
from .factory import DeliveryFactory
from .io import load
def main():
 p=argparse.ArgumentParser();p.add_argument("case");p.add_argument("--output");a=p.parse_args();r=DeliveryFactory().analyze(*load(a.case));s=json.dumps(r,indent=2,sort_keys=True)
 if a.output:Path(a.output).write_text(s+"\n")
 print(s)
if __name__=="__main__":main()

