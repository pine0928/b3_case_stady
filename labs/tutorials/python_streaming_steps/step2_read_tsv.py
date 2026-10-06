"""Step 2: read a saved TSV with Python's csv module."""
import csv, sys
from pathlib import Path

def iter_rows(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        yield from csv.reader(handle, delimiter="\t")

def main():
    if len(sys.argv)!=2: raise SystemExit("usage: python -m ...step2_read_tsv packets.tsv")
    for number,row in enumerate(iter_rows(sys.argv[1]),1): print(number,row)
if __name__=="__main__": main()
