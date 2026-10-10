"""Lab 5 student contract tests; experimental claims still require report review."""
import math
import pytest
from labs.lab5_compare import starter
from labs.lab5_compare.protocol import RepresentationConfig, CANONICAL_OBSERVABLES
from labs.lab5_compare.public_dataset import make_dataset


def test_student_interface():
    assert all(callable(getattr(starter, n)) for n in (
        'observable_budget', 'assert_matched_budget',
        'vectorize_your_representation', 'explain_advantage_type'))


def test_budget_is_declared_not_inferred_from_name():
    custom = RepresentationConfig('graph', observables=frozenset({'iat'}))
    assert starter.observable_budget(custom) == {'iat'}
    assert starter.observable_budget(RepresentationConfig('non-graph')) == set(CANONICAL_OBSERVABLES)


def test_equal_budgets_are_accepted():
    starter.assert_matched_budget(RepresentationConfig('sequence'), RepresentationConfig('graph'))


def test_unequal_budgets_rejected_with_explanation():
    a = RepresentationConfig('sequence')
    b = RepresentationConfig('graph', observables=frozenset({'iat', 'src_port'}))
    with pytest.raises(ValueError) as exc:
        starter.assert_matched_budget(a, b)
    assert 'graph' in str(exc.value) and 'sequence' in str(exc.value)


def test_vectorizer_finite_fixed_dimension_and_no_labels():
    data = make_dataset(n_per_class=3, seed=13)
    vectors = [tuple(starter.vectorize_your_representation(x.flow)) for x in data]
    assert vectors and len(vectors[0]) > 0
    assert all(len(v) == len(vectors[0]) for v in vectors)
    assert all(all(isinstance(z, (int, float)) and math.isfinite(z) for z in v) for v in vectors)


def test_conclusion_label_is_conservative_and_documented():
    assert starter.explain_advantage_type() in {'information', 'representation', 'model', 'confounded'}
