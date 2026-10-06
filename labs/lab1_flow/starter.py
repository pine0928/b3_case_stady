"""Lab 1 starter: PacketRecord -> observed bidirectional Flow instances."""
from collections.abc import Iterable, Iterator

from labs.common.schema import PacketRecord, Flow


def canonical_flow_key(packet: PacketRecord) -> tuple:
    """TODO: map forward/reverse packets to one stable bidirectional 5-tuple key."""
    raise NotImplementedError


def build_flows(records: list[PacketRecord], inactivity_timeout: float) -> list[Flow]:
    """Part 1A: TODO: construct Flow instances as a materialized list."""
    raise NotImplementedError


def iter_flows(records: Iterable[PacketRecord], inactivity_timeout: float) -> Iterator[Flow]:
    """Part 1B: TODO: yield completed Flow instances without materializing the input."""
    # Keep this function syntactically a generator while the implementation is TODO.
    if False:
        yield  # pragma: no cover
    raise NotImplementedError
