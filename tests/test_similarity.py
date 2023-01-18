from collections import OrderedDict

import numpy as np
import pytest

from inheritance_explorer.similarity import PycodeSimilarity, ResultsContainer


def test_results_container():

    results = {"a": 1, "b": "c", "c": 3}
    r = ResultsContainer(results)
    for key, val in results.items():
        assert getattr(r, key) == val


@pytest.fixture
def sample_source_dict():
    test_source = "def test_func(a, b, c):\n" "    return a * b * c"
    test_source2 = "def test_func(a, b, c):\n" "    a = a * 10\n" "    return a * b * c"
    test_source3 = "def test_func(a, b, c):\n" "    a = a * b\n" "    return a * b * c"
    source_dict = OrderedDict()
    source_dict["a"] = test_source
    source_dict["b"] = test_source
    source_dict["c"] = test_source2
    source_dict["d"] = test_source
    source_dict["e"] = test_source3

    N = len(source_dict)
    s_matrix = np.ones((N, N))
    s_matrix[2, 0] = 0
    s_matrix[4, 0] = 0
    s_matrix[2, 1] = 0
    s_matrix[4, 1] = 0
    s_matrix[0:2, 2] = 0
    s_matrix[3:, 2] = 0
    s_matrix[2, 3] = 0
    s_matrix[4, 3] = 0
    s_matrix[0:4, 4] = 0

    return source_dict, s_matrix.astype(bool)


def check_result(results, source_dict, ref, expected_match):
    for key, _ in source_dict.items():
        if key != ref:
            assert key in results
            f = results[key]
            if expected_match[key]:
                assert f.similarity_fraction == 1.0
            else:
                assert f.similarity_fraction < 1.0


def test_pycode_similarity_single_ref(sample_source_dict):

    s_dict, s_matrix = sample_source_dict
    ref = "a"
    p = PycodeSimilarity()
    results = p.run(s_dict, reference=ref)
    s_bool = dict(zip(s_dict.keys(), s_matrix[:, 0]))
    check_result(results, s_dict, ref, expected_match=s_bool)


def test_pycode_similarity_permuted(sample_source_dict):

    s_dict, s_bool = sample_source_dict
    p = PycodeSimilarity(method="permute")
    results, sim_matrix, sim_axis = p.run(s_dict)

    assert sim_matrix.shape == s_bool.shape

    bool_matrix = sim_matrix.astype(int).astype(bool)
    assert np.all(bool_matrix == s_bool)

    for k in s_dict.keys():
        assert k in sim_axis


def test_errors():
    with pytest.raises(ValueError, match="Provided method not recognized"):
        _ = PycodeSimilarity(method="badmethod")
