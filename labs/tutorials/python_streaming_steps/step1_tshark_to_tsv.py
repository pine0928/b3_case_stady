"""Step 1: print a shell command that materializes TShark output as TSV."""
from .common import FIELDS, SPEC

def main():
    parts = [
        "tshark -n -r labs/data/canonical_smoke.pcap",
        f"-Y '{SPEC.display_filter}'",
        "-T fields",
    ]
    parts += [f"-e {field}" for field in FIELDS]
    parts += ["-E 'separator=\t' -E quote=n -E occurrence=f", "> packets.tsv"]
    print(" ".join(parts))

if __name__ == "__main__":
    main()
