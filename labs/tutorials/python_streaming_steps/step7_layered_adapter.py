"""Step 7: the final public interface hides the ingestion engine downstream."""
import sys
from labs.common.tshark import iter_tshark_packet_records

def consume_packets(records):
    """Example downstream consumer: it knows PacketRecord, not TShark TSV."""
    count=total_bytes=0
    for packet in records:
        count += 1; total_bytes += packet.packet_length
    return count,total_bytes

def main():
    capture=sys.argv[1] if len(sys.argv)>1 else "labs/data/canonical_smoke.pcap"
    count,total=consume_packets(iter_tshark_packet_records(capture))
    print(f"packets={count} l3_bytes={total}")
if __name__=="__main__": main()
