"""Canonical educational idle-timeout sessionizer (capture order)."""
from collections.abc import Iterable, Iterator
from .schema import PacketRecord, Flow, DirectedPacket
from .preprocess import canonical_flow_key, endpoint


def iter_idle_flows(records: Iterable[PacketRecord], inactivity_timeout: float = 30.0) -> Iterator[Flow]:
    if inactivity_timeout <= 0:
        raise ValueError("inactivity_timeout must be positive")
    active: dict[tuple, tuple[Flow, tuple, float]] = {}
    previous_timestamp = None
    for p in records:
        if previous_timestamp is not None and p.timestamp < previous_timestamp:
            raise ValueError("packet timestamps must be nondecreasing in capture order")
        previous_timestamp = p.timestamp
        expired = [key for key, (_, _, last) in active.items()
                   if p.timestamp - last > inactivity_timeout]
        for key in sorted(expired, key=repr):
            yield active.pop(key)[0]
        key = canonical_flow_key(p)
        if key in active:
            flow, forward, last = active[key]
        else:
            flow, forward, last = Flow(key=key), endpoint(p, True), p.timestamp
        iat = 0.0 if not flow.packets else p.timestamp - last
        direction = 1 if endpoint(p, True) == forward else -1
        flow.packets.append(DirectedPacket(packet=p, direction=direction, iat=iat))
        active[key] = (flow, forward, p.timestamp)
    for key in sorted(active, key=repr):
        yield active[key][0]
