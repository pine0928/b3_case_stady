"""Lab 2 starter: flow -> alternative burst segmentations."""
from labs.common.schema import Flow, Burst


def direction_only_bursts(flow: Flow) -> list[Burst]:
    """TODO: maximal consecutive packet runs with identical direction."""
    raise NotImplementedError


def alternative_bursts(flow: Flow, **params) -> list[Burst]:
    """TODO: implement and document one IAT/ACK/payload-aware alternative."""
    raise NotImplementedError
