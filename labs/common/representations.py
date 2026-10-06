"""Shared non-graph representation data contracts for Lab 3.

The goal of these records is to make representation choices inspectable.  They
store not only numeric values, but also masks, feature names, and truncation
metadata so that later ML experiments can be traced back to the exact input
budget.

No third-party numerical library is required at this stage.  The records use
plain Python lists so students can inspect every transformation directly.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class StatisticalVector:
    feature_names: tuple[str, ...]
    values: tuple[float, ...]


@dataclass(frozen=True)
class PaddedSequence:
    """A fixed-length sequence plus an explicit validity mask."""

    feature_names: tuple[str, ...]
    values: tuple[tuple[float, ...], ...]
    mask: tuple[int, ...]
    original_length: int
    retained_length: int
    truncation: str

    @property
    def truncated(self) -> bool:
        return self.retained_length < self.original_length


@dataclass(frozen=True)
class HierarchicalBurst:
    """One burst with its summary features and packet-level observations."""

    direction: int
    burst_features: tuple[float, ...]
    packet_features: tuple[tuple[float, ...], ...]


@dataclass(frozen=True)
class HierarchicalRepresentation:
    """Ragged packet-within-burst hierarchy before batching/padding."""

    burst_feature_names: tuple[str, ...]
    packet_feature_names: tuple[str, ...]
    bursts: tuple[HierarchicalBurst, ...]

    @property
    def packet_count(self) -> int:
        return sum(len(b.packet_features) for b in self.bursts)


@dataclass(frozen=True)
class PaddedHierarchy:
    """Fixed-shape hierarchy suitable for a later neural batching layer."""

    burst_feature_names: tuple[str, ...]
    packet_feature_names: tuple[str, ...]
    burst_values: tuple[tuple[float, ...], ...]
    burst_mask: tuple[int, ...]
    packet_values: tuple[tuple[tuple[float, ...], ...], ...]
    packet_mask: tuple[tuple[int, ...], ...]
    original_bursts: int
    retained_bursts: int
    original_packets: int
    retained_packets: int

    @property
    def dropped_packets(self) -> int:
        return self.original_packets - self.retained_packets


@dataclass(frozen=True)
class ZScoreStats:
    """Training-set normalization parameters.

    `std` is floored to 1.0 for constant features so applying the transform is
    well-defined and does not create artificial large values.
    """

    feature_names: tuple[str, ...]
    mean: tuple[float, ...]
    std: tuple[float, ...]
    fitted_split: str = "train"
