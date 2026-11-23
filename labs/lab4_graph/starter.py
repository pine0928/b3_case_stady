"""Lab 4 student starter: explicit graph-construction decisions.

Every edge must document provenance using one or more of:
P protocol-grounded, O order-derived, B burst/cycle-derived,
A association-derived, L learned/adaptive, H designer-typed.
"""
from labs.common.graphs import GraphNode, GraphEdge, TrafficGraph


def packet_chain_graph(flow) -> TrafficGraph:
    """Create a directed graph connecting consecutive packets."""

    nodes = []
    edges = []

    # Create one node for each packet.
    for i, p in enumerate(flow.packets, start=1):
        nodes.append(
            GraphNode(
                node_id=f"p{i}",
                node_type="packet",
                feature_names=("direction", "packet_length", "iat"),
                features=(
                    float(p.direction),
                    float(p.packet.packet_length),
                    float(p.iat),
                ),
            )
        )

    # Connect each packet to the next packet.
    for i in range(len(flow.packets) - 1):
        edges.append(
            GraphEdge(
                src=f"p{i + 1}",
                dst=f"p{i + 2}",
                relation="next_packet",
                provenance=("O", "H"),
                feature_names=("target_iat",),
                features=(float(flow.packets[i + 1].iat),),
            )
        )

    return TrafficGraph(
        design="packet_chain",
        nodes=tuple(nodes),
        edges=tuple(edges),
        raw_observable_budget=("direction", "packet_length", "iat"),
        explicit_relations=("next_packet",),
        information_loss=(),
    )

def burst_graph(flow, bursts) -> TrafficGraph:
    """Create a directed graph connecting consecutive bursts."""

    # Check that bursts contain exactly the flow packets
    # in the original order.
    flattened = [
        packet
        for burst in bursts
        for packet in burst.packets
    ]

    if len(flattened) != len(flow.packets):
        raise ValueError("Bursts do not partition flow packets")

    if any(
        actual is not expected
        for actual, expected in zip(flattened, flow.packets)
    ):
        raise ValueError("Bursts do not preserve flow packet order")

    nodes = []
    edges = []

    # Create one node for each burst.
    for i, burst in enumerate(bursts, start=1):
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
            start_time = end_time = duration = 0.0

        if i == 1:
            gap = 0.0
        else:
            previous_packets = bursts[i - 2].packets
            if packets and previous_packets:
                previous_end = previous_packets[-1].packet.timestamp
                gap = start_time - previous_end
            else:
                gap = 0.0

        nodes.append(
            GraphNode(
                node_id=f"b{i}",
                node_type="burst",
                feature_names=(
                    "direction",
                    "packet_count",
                    "byte_count",
                    "duration",
                    "gap_from_previous_burst",
                ),
                features=(
                    float(burst.direction),
                    float(packet_count),
                    float(byte_count),
                    float(duration),
                    float(gap),
                ),
            )
        )

    # Connect consecutive bursts.
    for i in range(len(bursts) - 1):
        next_burst = bursts[i + 1]
        current_packets = bursts[i].packets
        next_packets = next_burst.packets

        if next_packets and current_packets:
            next_start = next_packets[0].packet.timestamp
            current_end = current_packets[-1].packet.timestamp
            gap = next_start - current_end
        else:
            gap = 0.0

        edges.append(
            GraphEdge(
                src=f"b{i + 1}",
                dst=f"b{i + 2}",
                relation="next_burst",
                provenance=("B", "O", "H"),
                feature_names=("target_direction", "gap"),
		features=(
		    1.0,
		    float(gap),
		),
            )
        )

    return TrafficGraph(
        design="burst_graph",
        nodes=tuple(nodes),
        edges=tuple(edges),
        raw_observable_budget=("direction", "packet_length", "iat"),
        explicit_relations=("next_burst",),
        information_loss=(
            "within-burst individual packet lengths",
            "within-burst individual IATs",
        ),
    )

def packet_burst_hierarchical_graph(flow, bursts) -> TrafficGraph:
    """Create a hierarchical graph containing packets and bursts."""

    # Validate that bursts partition the flow in the original order.
    flattened = [
        packet
        for burst in bursts
        for packet in burst.packets
    ]

    if len(flattened) != len(flow.packets):
        raise ValueError("Bursts do not partition flow packets")

    if any(
        actual is not expected
        for actual, expected in zip(flattened, flow.packets)
    ):
        raise ValueError("Bursts do not preserve flow packet order")

    nodes = []
    edges = []

    # Create packet nodes.
    for i, p in enumerate(flow.packets, start=1):
        nodes.append(
            GraphNode(
                node_id=f"p{i}",
                node_type="packet",
                feature_names=("direction", "packet_length", "iat"),
                features=(
                    float(p.direction),
                    float(p.packet.packet_length),
                    float(p.iat),
                ),
            )
        )

    # Create burst nodes.
    for i, burst in enumerate(bursts, start=1):
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
            start_time = end_time = duration = 0.0

        if i == 1:
            gap = 0.0
        else:
            previous_packets = bursts[i - 2].packets
            if packets and previous_packets:
                previous_end = previous_packets[-1].packet.timestamp
                gap = start_time - previous_end
            else:
                gap = 0.0

        nodes.append(
            GraphNode(
                node_id=f"b{i}",
                node_type="burst",
                feature_names=(
                    "direction",
                    "packet_count",
                    "byte_count",
                    "duration",
                    "gap_from_previous_burst",
                ),
                features=(
                    float(burst.direction),
                    float(packet_count),
                    float(byte_count),
                    float(duration),
                    float(gap),
                ),
            )
        )

    # Create next_packet edges.
    for i in range(len(flow.packets) - 1):
        edges.append(
            GraphEdge(
                src=f"p{i + 1}",
                dst=f"p{i + 2}",
                relation="next_packet",
                provenance=("O", "H"),
                feature_names=("target_iat",),
                features=(float(flow.packets[i + 1].iat),),
            )
        )

    # Create member_of edges.
    packet_index = 1
    for i, burst in enumerate(bursts, start=1):
        for _ in burst.packets:
            edges.append(
                GraphEdge(
                    src=f"p{packet_index}",
                    dst=f"b{i}",
                    relation="member_of",
                    provenance=("B", "H"),
                )
            )
            packet_index += 1

    # Create next_burst edges.
    for i in range(len(bursts) - 1):
        current_packets = bursts[i].packets
        next_packets = bursts[i + 1].packets

        if current_packets and next_packets:
            current_end = current_packets[-1].packet.timestamp
            next_start = next_packets[0].packet.timestamp
            gap = next_start - current_end
        else:
            gap = 0.0

        edges.append(
            GraphEdge(
                src=f"b{i + 1}",
                dst=f"b{i + 2}",
                relation="next_burst",
                provenance=("B", "O", "H"),
                feature_names=("target_direction", "gap"),
                features=(1.0, float(gap)),
            )
        )

    return TrafficGraph(
        design="packet_burst_hierarchical",
        nodes=tuple(nodes),
        edges=tuple(edges),
        raw_observable_budget=("direction", "packet_length", "iat"),
        explicit_relations=("next_packet", "member_of", "next_burst"),
        information_loss=(),
    )

