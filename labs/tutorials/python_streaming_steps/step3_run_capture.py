"""Step 3: simple automation with subprocess.run(). Suitable for small output."""
import subprocess, sys
from .common import build_command

def main():
    capture=sys.argv[1] if len(sys.argv)>1 else "labs/data/canonical_smoke.pcap"
    result=subprocess.run(build_command(capture), capture_output=True, text=True, encoding="utf-8", check=True)
    print(result.stdout, end="")
    if result.stderr: print("stderr:", result.stderr, file=sys.stderr)
if __name__=="__main__": main()
