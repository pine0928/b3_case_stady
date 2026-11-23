"""Lab 1 starter: PacketRecord -> observed bidirectional Flow instances."""
import ipaddress
from collections.abc import Iterable, Iterator

from labs.common.schema import PacketRecord, Flow, DirectedPacket


def canonical_flow_key(packet: PacketRecord) -> tuple:
    """Return a stable bidirectional 5-tuple key."""
    a = (packet.src_ip, packet.src_port)
    b = (packet.dst_ip, packet.dst_port)

    def endpoint_sort_key(endpoint: tuple) -> tuple:
        ip, port = endpoint
        address = ipaddress.ip_address(ip)
        return (
            address.version,
            int(address),
            -1 if port is None else port,
        )

    lower, higher = sorted((a, b), key=endpoint_sort_key)

    return (packet.protocol, lower, higher)

def build_flows(records: list[PacketRecord], inactivity_timeout: float) -> list[Flow]:
    """Construct Flow instances using an inactivity timeout."""
    if inactivity_timeout <= 0:
        raise ValueError("inactivity_timeout must be positive")

    active = {}
    completed = []
    previous_timestamp = None

    for packet in records:
        # Check capture order.
        if previous_timestamp is not None and packet.timestamp < previous_timestamp:
            raise ValueError("packet timestamps must be nondecreasing")
        previous_timestamp = packet.timestamp

        # Finalize flows that exceeded the inactivity timeout.
        expired = [
            key
            for key, (_, _, last) in active.items()
            if packet.timestamp - last > inactivity_timeout
        ]

        for key in sorted(expired, key=repr):
            completed.append(active.pop(key)[0])

        # Identify the bidirectional flow.
        key = canonical_flow_key(packet)

        if key in active:
            flow, forward, last = active[key]
        else:
            flow = Flow(key=key, packets=[])
            forward = (packet.src_ip, packet.src_port)
            last = packet.timestamp

        # Calculate direction and flow-local IAT.
        iat = 0.0 if not flow.packets else packet.timestamp - last
        source = (packet.src_ip, packet.src_port)
        direction = 1 if source == forward else -1

        flow.packets.append(
            DirectedPacket(packet=packet, direction=direction, iat=iat)
        )

        # Update the active flow.
        active[key] = (flow, forward, packet.timestamp)

    # Finalize remaining flows at EOF.
    for key in sorted(active, key=repr):
        completed.append(active[key][0])

    return completed


def iter_flows(records: Iterable[PacketRecord], inactivity_timeout: float) -> Iterator[Flow]:
    """Yield completed Flow instances without materializing the input."""
    if inactivity_timeout <= 0:
        raise ValueError("inactivity_timeout must be positive")

    active = {}
    previous_timestamp = None

    for packet in records:
        # Check capture order.
        if previous_timestamp is not None and packet.timestamp < previous_timestamp:
            raise ValueError("packet timestamps must be nondecreasing")
        previous_timestamp = packet.timestamp

        # Find flows that exceeded the inactivity timeout.
        expired = [
            key
            for key, (_, _, last) in active.items()
            if packet.timestamp - last > inactivity_timeout
        ]

        # Yield expired flows immediately.
        for key in sorted(expired, key=repr):
            yield active.pop(key)[0]

        # Identify the bidirectional flow.
        key = canonical_flow_key(packet)

        if key in active:
            flow, forward, last = active[key]
        else:
            flow = Flow(key=key, packets=[])
            forward = (packet.src_ip, packet.src_port)
            last = packet.timestamp

        # Calculate direction and flow-local IAT.
        iat = 0.0 if not flow.packets else packet.timestamp - last
        source = (packet.src_ip, packet.src_port)
        direction = 1 if source == forward else -1

        flow.packets.append(
            DirectedPacket(packet=packet, direction=direction, iat=iat)
        )

        # Update active flow state.
        active[key] = (flow, forward, packet.timestamp)

    # Yield all remaining flows at EOF.
    for key in sorted(active, key=repr):
        yield active[key][0]
