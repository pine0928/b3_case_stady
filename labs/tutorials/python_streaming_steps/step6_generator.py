"""Step 6: expose packet records lazily with yield."""
import sys
from labs.common.tshark import iter_tshark_packet_records

def first_records(path, limit=3):
    for index,record in enumerate(iter_tshark_packet_records(path)):
        if index >= limit: return
        yield record

def main():
    capture=sys.argv[1] if len(sys.argv)>1 else "labs/data/canonical_smoke.pcap"
    records=first_records(capture)
    print("generator object:", records)
    for record in records: print(record)
if __name__=="__main__": main()
