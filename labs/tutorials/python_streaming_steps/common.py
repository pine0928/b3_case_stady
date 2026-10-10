"""Shared command construction for tutorial Steps 1-6.

Kept small so students can see that command construction is separate from
process execution and row parsing.
"""
from pathlib import Path
import shutil

from labs.common.field_spec import FieldSpec
from labs.common.tshark import DEFAULT_FIELD_SPEC

SPEC = FieldSpec.from_yaml(DEFAULT_FIELD_SPEC)
FIELDS = SPEC.tshark_fields

def build_command(capture: str | Path, tshark_path: str="tshark") -> list[str]:
    exe=shutil.which(tshark_path)
    if not exe:
        raise RuntimeError("TShark not found on PATH")
    cmd=[exe,"-n","-r",str(capture),"-Y",SPEC.display_filter,"-T","fields"]
    for field in FIELDS: cmd += ["-e",field]
    cmd += ["-E","separator=\t","-E","quote=n","-E","occurrence=f"]
    return cmd
