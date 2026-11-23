"""Lab 2 starter: flow -> alternative burst segmentations."""
from labs.common.schema import Flow, Burst


def direction_only_bursts(flow: Flow) -> list[Burst]:
    """Split a flow into maximal consecutive runs of identical direction."""
    bursts = []
    current_burst = None

    for dp in flow.packets:
        if current_burst is None or dp.direction != current_burst.direction:
            current_burst = Burst(direction=dp.direction, packets=[])
            bursts.append(current_burst)

        current_burst.packets.append(dp)

    return bursts


def alternative_bursts(flow: Flow, **params) -> list[Burst]:
    """
    Split a flow when direction changes or the IAT exceeds max_gap.

    max_gap: maximum allowed inter-arrival time within a burst, in seconds.
             Must be non-negative. Default: 0.01 seconds.
    """
    max_gap = params.get("max_gap", 0.01)

    if max_gap < 0:
        raise ValueError("max_gap must be non-negative")

    bursts = []
    current_burst = None

    for dp in flow.packets:
        if (
            current_burst is None
            or dp.direction != current_burst.direction
            or dp.iat > max_gap
        ):
            current_burst = Burst(direction=dp.direction, packets=[])
            bursts.append(current_burst)

        current_burst.packets.append(dp)

    return bursts
