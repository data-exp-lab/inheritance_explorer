from inheritance_explorer.similarity import PycodeSimilarity, ResultsContainer


def test_results_container():

    results = {"a": 1, "b": "c", "c": 3}
    r = ResultsContainer(results)
    for key, val in results.items():
        assert(getattr(r, key) == val)

def test_pycode_similarity_single_ref():

    def check_tuple_result(p, source_tuples, ref, should_match=True):
        for src_tupe in source_tuples:
            if src_tupe[0] != ref:
                assert (hasattr(p.results, src_tupe[0]))
                f = getattr(p.results, src_tupe[0])
                if should_match:
                    assert (f.similarity_fraction == 1.0)
                else:
                    assert (f.similarity_fraction < 1.0)

    p = PycodeSimilarity()

    test_source = "def test_func(a, b, c):\n" \
                  "    return a * b * c"

    source_tuples = [
        ("a", test_source),
        ("b", test_source),
        ("c", test_source)
    ]

    for ref in ["a", "b", "c"]:
        p.run(source_tuples, reference=ref)
        check_tuple_result(p, source_tuples, ref)

    test_source2 = "def test_func(a, b, c):\n" \
                   "    a = a * 10\n" \
                   "    return a * b * c"

    source_tuples += [("d", test_source2), ]
    p.run(source_tuples, reference="d")
    check_tuple_result(p, source_tuples, "d", should_match=False)


def test_pycode_similarity_premute():

    def check_tuple_result(p, source_tuples, ref, should_match=True):
        for src_tupe in source_tuples:
            if src_tupe[0] != ref:
                assert (hasattr(p.results, src_tupe[0]))
                f = getattr(p.results, src_tupe[0])
                if should_match:
                    assert (f.similarity_fraction == 1.0)
                else:
                    assert (f.similarity_fraction < 1.0)

    p = PycodeSimilarity(method="permute")

    test_source = "def test_func(a, b, c):\n" \
                  "    return a * b * c"


    test_source2 = "def test_func(a, b, c):\n" \
                   "    a = a * 10\n" \
                   "    return a * b * c"

    source_tuples = [
        ("_1", test_source),
        ("_2", test_source),
        ("_3", test_source),
        ("_4", test_source2)
    ]

    p.run(source_tuples)

