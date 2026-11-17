"""Lab 0 starter: TShark fields -> PacketRecord.

The PCAP dissection is delegated to TShark.  Your job is to understand the
selected protocol fields and map one tab-separated TShark row into the stable
PacketRecord contract used by later labs.
"""
from labs.common.schema import PacketRecord

# This order is the TSV contract.  Compare each name with the same field in
# Wireshark before implementing parse_tshark_row().
# Field names and ordering are declared once in the shared YAML FieldSpec.
# Students still implement the conversion from a TSV row to PacketRecord.
from labs.common.field_spec import FieldSpec
from labs.common.tshark import DEFAULT_FIELD_SPEC

TSHARK_FIELDS = FieldSpec.from_yaml(DEFAULT_FIELD_SPEC).tshark_fields


def parse_tshark_row(line: str) -> PacketRecord:
    """TODO: convert one tab-separated TShark fields row to PacketRecord.

    Requirements are defined in SPECIFICATION.md.  In particular, decide from
    ip.proto whether TCP or UDP fields are meaningful; do not treat empty TCP
    columns in a UDP row (or vice versa) as zero-valued observations.
    """

    # 1. タブで区切って14列に分割する
    values = line.rstrip("\n").split("\t")

    if len(values) != 14:
        raise ValueError("Invalid number of TSV columns")

    # 2. 各列の値を取り出す
    timestamp = float(values[0])
    src_ip = values[1]
    dst_ip = values[2]
    ip_proto = int(values[3])
    ip_length = int(values[4])

    # 3. プロトコルによって使用する列を切り替える
    if ip_proto == 6:
        protocol = "TCP"
        src_port = int(values[5])
        dst_port = int(values[6])
        payload_length = int(values[7])
        tcp_flags = int(values[8], 0)

    elif ip_proto == 17:
        protocol = "UDP"
        src_port = int(values[9])
        dst_port = int(values[10])
        udp_length = int(values[11])
        payload_length = max(0, udp_length - 8)
        tcp_flags = None

    else:
        raise ValueError("Unsupported IP protocol")

    # 4. キャプチャが途中で切れていないか確認する
    cap_len = int(values[12])
    frame_len = int(values[13])

    if cap_len < frame_len:
        raise ValueError("Snaplen-truncated packet")

    # 5. PacketRecordを作成して返す
    return PacketRecord(
        timestamp=timestamp,
        src_ip=src_ip,
        dst_ip=dst_ip,
        src_port=src_port,
        dst_port=dst_port,
        protocol=protocol,
        packet_length=ip_length,
        payload_length=payload_length,
        tcp_flags=tcp_flags,
    )
    raise NotImplementedError


def inter_arrival_times(records: list[PacketRecord]) -> list[float]:
    """TODO: return non-negative IATs after timestamp ordering; first IAT = 0."""

    # 1. パケットが空なら空のリストを返す
    if not records:
        return []

    # 2. timestampの昇順に並べ替える
    sorted_records = sorted(records, key=lambda record: record.timestamp)

    # 3. 最初のIATは0.0
    iats = [0.0]

    # 4. 隣り合うパケットの時間差を計算する
    for i in range(1, len(sorted_records)):
        difference = (
            sorted_records[i].timestamp
            - sorted_records[i - 1].timestamp
        )

        # 負の値にならないようにする
        iats.append(max(0.0, difference))
    return iats	
    raise NotImplementedError
