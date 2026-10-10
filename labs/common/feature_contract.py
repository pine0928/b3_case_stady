"""Canonical feature-name contracts shared across Lab 3 and Lab 4.

These are observable feature labels, not a reference implementation.
"""

PACKET_FEATURES = ("direction", "packet_length", "iat")
BURST_FEATURES = (
    "direction",
    "packet_count",
    "byte_count",
    "duration",
    "gap_from_previous_burst",
)
