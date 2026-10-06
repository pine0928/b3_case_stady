"""Step 4: keep the child alive and consume stdout incrementally."""
import subprocess, sys
from .common import build_command

def main():
    capture=sys.argv[1] if len(sys.argv)>1 else "labs/data/canonical_smoke.pcap"
    proc=subprocess.Popen(build_command(capture), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    assert proc.stdout is not None
    for number,line in enumerate(proc.stdout,1): print(number,line.rstrip("\n"))
    proc.stdout.close(); stderr=proc.stderr.read() if proc.stderr else ""; rc=proc.wait()
    if proc.stderr: proc.stderr.close()
    if rc: raise RuntimeError(f"TShark exit={rc}: {stderr.strip()}")
if __name__=="__main__": main()
