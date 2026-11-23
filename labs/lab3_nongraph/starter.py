"""Lab 3 starter: non-graph representation builders.

Students implement the same interfaces as the instructor reference in
`reference.py`.  Keep the canonical observable budget unless an extension is
explicitly declared and compared separately.
"""
from labs.common.schema import Flow, Burst
from labs.common.representations import (StatisticalVector, PaddedSequence,
HierarchicalBurst, HierarchicalRepresentation, PaddedHierarchy)

def statistical_vector(flow: Flow):
    packets = flow.packets

    feature_names = (
        "packet_count",
        "forward_packet_count",
        "backward_packet_count",
        "total_bytes",
        "forward_bytes",
        "backward_bytes",
        "mean_packet_length",
        "std_packet_length",
        "mean_iat",
        "std_iat",
        "flow_duration",
        "direction_switch_count",
    )

    lengths = [float(p.packet.packet_length) for p in packets]
    iats = [float(p.iat) for p in packets]

    packet_count = len(packets)

    forward_packets = [p for p in packets if p.direction == 1]
    backward_packets = [p for p in packets if p.direction == -1]

    forward_lengths = [float(p.packet.packet_length) for p in forward_packets]
    backward_lengths = [float(p.packet.packet_length) for p in backward_packets]

    total_bytes = sum(lengths)
    forward_bytes = sum(forward_lengths)
    backward_bytes = sum(backward_lengths)

    mean_length = sum(lengths) / packet_count if packet_count else 0.0
    mean_iat = sum(iats) / len(iats) if iats else 0.0

    std_length = (
        (sum((x - mean_length) ** 2 for x in lengths) / packet_count) ** 0.5
        if packet_count else 0.0
    )

    std_iat = (
        (sum((x - mean_iat) ** 2 for x in iats) / len(iats)) ** 0.5
        if iats else 0.0
    )

    if packets:
        flow_duration = (
            packets[-1].packet.timestamp - packets[0].packet.timestamp
        )
    else:
        flow_duration = 0.0

    direction_switch_count = sum(
        packets[i].direction != packets[i - 1].direction
        for i in range(1, packet_count)
    )

    values = (
        float(packet_count),
        float(len(forward_packets)),
        float(len(backward_packets)),
        float(total_bytes),
        float(forward_bytes),
        float(backward_bytes),
        mean_length,
        std_length,
        mean_iat,
        std_iat,
        float(flow_duration),
        float(direction_switch_count),
    )

    return StatisticalVector(
        feature_names=feature_names,
        values=values,
    )

def packet_sequence(flow: Flow, max_packets: int):
    if max_packets <= 0:
        raise ValueError("max_packets must be positive")

    packets = flow.packets

    original_length = len(packets)
    retained_packets = packets[:max_packets]
    retained_length = len(retained_packets)

    values = [
        (
            float(p.direction),
            float(p.packet.packet_length),
            float(p.iat),
        )
        for p in retained_packets
    ]

    mask = [1] * retained_length

    padding_count = max_packets - retained_length

    values.extend([(0.0, 0.0, 0.0)] * padding_count)
    mask.extend([0] * padding_count)

    return PaddedSequence(
        feature_names=("direction", "packet_length", "iat"),
        values=tuple(values),
        mask=tuple(mask),
        original_length=original_length,
        retained_length=retained_length,
        truncation="head",
    )


def burst_sequence(bursts: list[Burst], max_bursts: int):
    if max_bursts <= 0:
        raise ValueError("max_bursts must be positive")

    feature_names = (
        "direction",
        "packet_count",
        "byte_count",
        "duration",
        "gap_from_previous_burst",
    )

    original_length = len(bursts)
    retained_bursts = bursts[:max_bursts]
    retained_length = len(retained_bursts)

    values = []

    for i, burst in enumerate(retained_bursts):
        packets = burst.packets

        packet_count = len(packets)

        byte_count = sum(
            p.packet.packet_length for p in packets
        )

        if packets:
            start_time = packets[0].packet.timestamp
            end_time = packets[-1].packet.timestamp
            duration = end_time - start_time
        else:
            start_time = 0.0
            end_time = 0.0
            duration = 0.0

        if i == 0:
            gap = 0.0
        else:
            previous_packets = retained_bursts[i - 1].packets

            if packets and previous_packets:
                previous_end = previous_packets[-1].packet.timestamp
                gap = start_time - previous_end
            else:
                gap = 0.0

        values.append((
            float(burst.direction),
            float(packet_count),
            float(byte_count),
            float(duration),
            float(gap),
        ))

    padding_count = max_bursts - retained_length

    values.extend([(0.0, 0.0, 0.0, 0.0, 0.0)] * padding_count)

    mask = [1] * retained_length + [0] * padding_count

    return PaddedSequence(
        feature_names=feature_names,
        values=tuple(values),
        mask=tuple(mask),
        original_length=original_length,
        retained_length=retained_length,
        truncation="head",
    )


def hierarchical_representation(flow: Flow, bursts: list[Burst]): 
    packet_feature_names = (
        "direction",
        "packet_length",
        "iat",
    )

    burst_feature_names = (
        "direction",
        "packet_count",
        "byte_count",
        "duration",
        "gap_from_previous_burst",
    )

    # Flowのパケットを順番に確認できるようにする
    flow_packets = flow.packets

    # Burstに含まれるパケットがFlowと完全に一致するか確認
    flattened_packets = [
        packet
        for burst in bursts
        for packet in burst.packets
    ]

    if len(flattened_packets) != len(flow_packets):
        raise ValueError("Bursts do not partition flow packets")

    if any(
        actual is not expected
        for actual, expected in zip(flattened_packets, flow_packets)
    ):
        raise ValueError("Bursts do not preserve flow packet order")

    hierarchical_bursts = []

    for i, burst in enumerate(bursts):
        packets = burst.packets

        packet_features = tuple(
            (
                float(p.direction),
                float(p.packet.packet_length),
                float(p.iat),
            )
            for p in packets
        )

        packet_count = len(packets)

        byte_count = sum(
            p.packet.packet_length for p in packets
        )

        if packets:
            start_time = packets[0].packet.timestamp
            end_time = packets[-1].packet.timestamp
            duration = end_time - start_time
        else:
            start_time = 0.0
            end_time = 0.0
            duration = 0.0

        if i == 0:
            gap = 0.0
        else:
            previous_packets = bursts[i - 1].packets

            if packets and previous_packets:
                previous_end = previous_packets[-1].packet.timestamp
                gap = start_time - previous_end
            else:
                gap = 0.0

        burst_features = (
            float(burst.direction),
            float(packet_count),
            float(byte_count),
            float(duration),
            float(gap),
        )

        hierarchical_bursts.append(
            HierarchicalBurst(
                direction=burst.direction,
                burst_features=burst_features,
                packet_features=packet_features,
            )
        )

    return HierarchicalRepresentation(
        burst_feature_names=burst_feature_names,
        packet_feature_names=packet_feature_names,
        bursts=tuple(hierarchical_bursts),
    )

def pad_hierarchy(rep, max_bursts: int, max_packets_per_burst: int):
    if max_bursts <= 0:
        raise ValueError("max_bursts must be positive")

    if max_packets_per_burst <= 0:
        raise ValueError("max_packets_per_burst must be positive")

    original_bursts = len(rep.bursts)
    original_packets = rep.packet_count

    retained_bursts = rep.bursts[:max_bursts]
    retained_burst_count = len(retained_bursts)

    burst_values = []
    burst_mask = []

    packet_values = []
    packet_mask = []

    retained_packets = 0

    for burst in retained_bursts:
        burst_values.append(burst.burst_features)
        burst_mask.append(1)

        retained_packet_features = burst.packet_features[
            :max_packets_per_burst
        ]

        retained_count = len(retained_packet_features)
        retained_packets += retained_count

        padded_packets = list(retained_packet_features)
        padded_mask = [1] * retained_count

        padding_count = max_packets_per_burst - retained_count

        padded_packets.extend(
            [(0.0, 0.0, 0.0)] * padding_count
        )
        padded_mask.extend([0] * padding_count)

        packet_values.append(tuple(padded_packets))
        packet_mask.append(tuple(padded_mask))

    # 不足するBurstをPaddingする
    burst_padding_count = max_bursts - retained_burst_count

    burst_values.extend(
        [(0.0,) * len(rep.burst_feature_names)] * burst_padding_count
    )
    burst_mask.extend([0] * burst_padding_count)

    packet_values.extend(
        [
            tuple(
                [(0.0,) * len(rep.packet_feature_names)]
                * max_packets_per_burst
            )
        ] * burst_padding_count
    )

    packet_mask.extend(
        [
            tuple([0] * max_packets_per_burst)
        ] * burst_padding_count
    )

    return PaddedHierarchy(
        burst_feature_names=rep.burst_feature_names,
        packet_feature_names=rep.packet_feature_names,
        burst_values=tuple(burst_values),
        burst_mask=tuple(burst_mask),
        packet_values=tuple(packet_values),
        packet_mask=tuple(packet_mask),
        original_bursts=original_bursts,
        retained_bursts=retained_burst_count,
        original_packets=original_packets,
        retained_packets=retained_packets,
    )
