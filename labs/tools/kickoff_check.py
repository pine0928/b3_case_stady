"""Kickoff environment check for the TShark-first B3 course path."""
from __future__ import annotations

import hashlib
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PCAP = ROOT / "labs" / "data" / "canonical_smoke.pcap"


def main() -> int:
    failures: list[str] = []
    print("B3 KICKOFF CHECK")
    print(f"Python: {platform.python_version()}")
    print(f"Platform: {platform.platform()}")

    if sys.version_info < (3, 11):
        failures.append("Python 3.11 or newer is recommended")

    try:
        print(subprocess.check_output(["git", "--version"], text=True).strip())
    except (OSError, subprocess.CalledProcessError):
        failures.append("Git command is not available")

    tshark = shutil.which("tshark")
    if not tshark:
        failures.append("TShark is not available on PATH; install Wireshark/TShark")
    else:
        try:
            print(subprocess.check_output([tshark, "--version"], text=True).splitlines()[0])
        except (OSError, subprocess.CalledProcessError):
            failures.append("TShark exists but could not be executed")

    if not PCAP.exists():
        failures.append(f"Canonical PCAP is missing: {PCAP}")
    else:
        print(f"Canonical PCAP SHA256: {hashlib.sha256(PCAP.read_bytes()).hexdigest()}")
        if tshark:
            try:
                proc = subprocess.run(
                    [tshark, "-n", "-r", str(PCAP),
                     "-Y", "ip && (tcp || udp) && ip.flags.mf == 0 && ip.frag_offset == 0",
                     "-T", "fields", "-e", "ip.proto"],
                    text=True, capture_output=True, check=True,
                )
                protocols = [x.strip() for x in proc.stdout.splitlines() if x.strip()]
                tcp, udp = protocols.count("6"), protocols.count("17")
                print(f"TShark baseline packets: {len(protocols)} (TCP={tcp}, UDP={udp})")
                if (len(protocols), tcp, udp) != (7, 5, 2):
                    failures.append("Canonical TShark counts differ from the frozen baseline")
            except subprocess.CalledProcessError as exc:
                failures.append(f"TShark could not read the canonical PCAP: {exc.stderr.strip()}")

    if failures:
        print("\nSTATUS: CHECK / ASK")
        for item in failures:
            print(f"- {item}")
        return 1

    print("\nSTATUS: PASS")
    print("Setup only: Wireshark/TShark observation path is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
