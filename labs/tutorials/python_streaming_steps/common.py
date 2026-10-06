"""Shared command construction for tutorial Steps 1-6.

Kept small so students can see that command construction is separate from
process execution and row parsing.
"""
from pathlib import Path
import shutil

FIELDS=("frame.time_epoch","ip.src","ip.dst","ip.proto","ip.len","tcp.srcport","tcp.dstport","tcp.len","tcp.flags","udp.srcport","udp.dstport","udp.length","frame.cap_len","frame.len")

def build_command(capture: str | Path, tshark_path: str="tshark") -> list[str]:
    exe=shutil.which(tshark_path)
    if not exe:
        raise RuntimeError("TShark not found on PATH")
    cmd=[exe,"-n","-r",str(capture),"-Y","ip && (tcp || udp) && !ip.flags.mf && ip.frag_offset == 0","-T","fields"]
    for field in FIELDS: cmd += ["-e",field]
    cmd += ["-E","separator=\t","-E","quote=n","-E","occurrence=f"]
    return cmd
