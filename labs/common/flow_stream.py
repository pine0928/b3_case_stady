"""Bounded-state 5-tuple flow/burst tracking."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import heapq
from typing import Iterable, Iterator

from .schema import Burst, DirectedPacket, Flow, PacketRecord
from .preprocess import canonical_flow_key, endpoint

class TerminationReason(str, Enum):
    IDLE_TIMEOUT = "idle_timeout"
    TCP_RST = "tcp_rst"
    TCP_FIN = "tcp_fin"
    EOF = "eof"

@dataclass(frozen=True)
class FlowTermination:
    reason: TerminationReason
    fin_fw_seen: bool = False
    fin_bw_seen: bool = False
    rst_seen: bool = False

@dataclass
class _ActiveFlow:
    flow_id: int
    key: tuple
    forward_endpoint: tuple
    first_timestamp: float
    last_timestamp: float
    packets: list[DirectedPacket] = field(default_factory=list)
    completed_bursts: list[Burst] = field(default_factory=list)
    current_burst: Burst | None = None
    fin_fw_seen: bool = False
    fin_bw_seen: bool = False
    rst_seen: bool = False
    closing: bool = False
    generation: int = 0

    def add(self, packet: PacketRecord, burst_max_gap: float | None) -> None:
        direction = +1 if endpoint(packet, True) == self.forward_endpoint else -1
        iat = max(0.0, packet.timestamp - self.last_timestamp) if self.packets else 0.0
        dp = DirectedPacket(packet=packet, direction=direction, iat=iat)
        self.packets.append(dp)
        split = self.current_burst is None or self.current_burst.direction != direction or (
            burst_max_gap is not None and iat > burst_max_gap
        )
        if split:
            if self.current_burst is not None:
                self.completed_bursts.append(self.current_burst)
            self.current_burst = Burst(direction=direction, packets=[])
        self.current_burst.packets.append(dp)
        self.last_timestamp = packet.timestamp
        self.generation += 1

        if packet.protocol.upper() == "TCP" and packet.tcp_flags is not None:
            flags = packet.tcp_flags
            if flags & 0x04:  # RST
                self.rst_seen = True
            if flags & 0x01:  # FIN
                if direction == +1:
                    self.fin_fw_seen = True
                else:
                    self.fin_bw_seen = True
                self.closing = self.fin_fw_seen and self.fin_bw_seen

    def finish(self, reason: TerminationReason) -> "CompletedFlow":
        bursts = list(self.completed_bursts)
        if self.current_burst is not None:
            bursts.append(self.current_burst)
        return CompletedFlow(
            flow_id=self.flow_id,
            flow=Flow(key=self.key, packets=self.packets),
            bursts=tuple(bursts),
            termination=FlowTermination(reason, self.fin_fw_seen, self.fin_bw_seen, self.rst_seen),
        )

@dataclass(frozen=True)
class CompletedFlow:
    flow_id: int
    flow: Flow
    bursts: tuple[Burst, ...]
    termination: FlowTermination


def iter_completed_flows(
    records: Iterable[PacketRecord], *, inactivity_timeout: float = 30.0,
    burst_max_gap: float | None = None, closing_timeout: float = 1.0,
) -> Iterator[CompletedFlow]:
    """Yield observed 5-tuple flow instances as their lifecycle completes."""
    if inactivity_timeout <= 0:
        raise ValueError("inactivity_timeout must be positive")
    if burst_max_gap is not None and burst_max_gap < 0:
        raise ValueError("burst_max_gap must be non-negative")
    if closing_timeout < 0:
        raise ValueError("closing_timeout must be non-negative")

    active: dict[tuple, _ActiveFlow] = {}
    expiry_heap: list[tuple[float, int, int, tuple]] = []
    next_flow_id = 0

    def schedule(state: _ActiveFlow) -> None:
        timeout = closing_timeout if state.closing else inactivity_timeout
        heapq.heappush(expiry_heap, (state.last_timestamp + timeout, state.flow_id, state.generation, state.key))

    def expire_due(now: float):
        while expiry_heap and expiry_heap[0][0] < now:
            _, flow_id, generation, key = heapq.heappop(expiry_heap)
            state = active.get(key)
            # Updates leave older heap entries behind.  Identity + generation
            # make those entries harmless without O(n) heap deletion.
            if state is None or state.flow_id != flow_id or state.generation != generation:
                continue
            active.pop(key)
            reason = TerminationReason.TCP_FIN if state.closing else TerminationReason.IDLE_TIMEOUT
            yield state.finish(reason)

    previous_timestamp = None
    for packet in records:
        if previous_timestamp is not None and packet.timestamp < previous_timestamp:
            raise ValueError("packet timestamps must be nondecreasing in capture order")
        previous_timestamp = packet.timestamp
        now = packet.timestamp
        yield from expire_due(now)

        key = canonical_flow_key(packet)
        state = active.get(key)
        if state is None:
            state = _ActiveFlow(next_flow_id, key, endpoint(packet, True), now, now)
            next_flow_id += 1
            active[key] = state
        state.add(packet, burst_max_gap)
        if state.rst_seen:
            active.pop(key)
            yield state.finish(TerminationReason.TCP_RST)
        else:
            schedule(state)

    for key in sorted(active, key=repr):
        yield active[key].finish(TerminationReason.EOF)


def iter_flows(records: Iterable[PacketRecord], **kwargs) -> Iterator[Flow]:
    for completed in iter_completed_flows(records, **kwargs):
        yield completed.flow


def iter_flow_bursts(records: Iterable[PacketRecord], **kwargs) -> Iterator[tuple[Flow, tuple[Burst, ...]]]:
    for completed in iter_completed_flows(records, **kwargs):
        yield completed.flow, completed.bursts
