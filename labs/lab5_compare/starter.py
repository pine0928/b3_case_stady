"""Lab 5 student starter: matched-information comparison contract."""
from labs.lab5_compare.protocol import RepresentationConfig


def observable_budget(config: RepresentationConfig) -> set[str]:
    """TODO: return the raw observables exposed to a representation."""
    raise NotImplementedError


def assert_matched_budget(config_a: RepresentationConfig, config_b: RepresentationConfig):
    """TODO: fail when compared representations receive different observables."""
    raise NotImplementedError


def vectorize_your_representation(flow):
    """TODO: return a fixed-length vector without silently adding raw fields."""
    raise NotImplementedError


def explain_advantage_type() -> str:
    """TODO: classify an observed difference as information/representation/model/confounded."""
    raise NotImplementedError
