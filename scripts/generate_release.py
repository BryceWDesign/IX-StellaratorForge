from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run(*args:str)->None:
 subprocess.run([sys.executable,*args],cwd=ROOT,check=True)

def main()->int:
 # Preserve/reproduce IX-Fusion foundation evidence.
 run('scripts/run_poc.py')
 run('scripts/run_secondary_studies.py')
 # Rebuild current StellaratorForge evidence.
 run('scripts/run_sfr1_poc.py')
 run('scripts/run_closure_campaign.py')
 run('scripts/run_computational_closure.py')
 run('scripts/generate_v040_evidence.py')
 run('scripts/make_manifest.py')
 print('IX-StellaratorForge v0.4.0 release artifacts regenerated')
 return 0
if __name__=='__main__':raise SystemExit(main())
