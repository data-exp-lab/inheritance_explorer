import abc
import collections
from typing import Any, Optional, OrderedDict

import numpy as np
import numpy.typing as npt
import pycode_similar


class ResultsContainer:
    def __init__(
        self,
        count: int,
        total: int,
        similarity_fraction: float,
        base_class: int,
        this_class: int,
    ):
        self.count = count
        self.total = total
        self.similarity_fraction = similarity_fraction
        self.base_class = base_class
        self.this_class = this_class


_sdict_type = OrderedDict[int, str]

_nested_source_dict = dict[int, OrderedDict[int, ResultsContainer]]

_sim_results_tuple = tuple[
    _nested_source_dict,
    npt.NDArray[Any],
    tuple[int, ...],
]


_single_result = OrderedDict[int, ResultsContainer]


class SimilarityContainer(abc.ABC):

    _valid_methods: list[str] = ["permute", "reference"]

    def __init__(self, method: str = "reference"):
        if method not in self._valid_methods:
            raise ValueError(
                f"Provided method not recognized, must be in {self._valid_methods}"
            )
        self.method = method
        self.results = None  # for storing results of similarity tests

    def run(
        self, source_dict: _sdict_type, reference: Optional[Any] = None
    ) -> _single_result | _sim_results_tuple:
        """
        source_dict : dict
            dictionary mapping a node identifier to a source code string
        """

        source_dict_c = source_dict.copy()
        results: _single_result | _sim_results_tuple
        if self.method == "permute":
            results = self._permute_and_run(source_dict_c)
        else:
            if reference not in source_dict_c or reference is None:
                raise ValueError(
                    "The the reference parameter must be a key in source_dict"
                )
            results = self._compare_single_set(source_dict_c, reference)
        return results

    @abc.abstractmethod
    def _permute_and_run(self, source_dict: _sdict_type) -> _sim_results_tuple:
        pass

    @abc.abstractmethod
    def _compare_single_set(
        self, source_dict: _sdict_type, reference: Any
    ) -> _single_result:
        pass


class PycodeSimilarity(SimilarityContainer):
    def _compare_single_set(
        self,
        source_dict: _sdict_type,
        reference: int,
    ) -> _single_result:

        src = source_dict[reference]  # extract the reference
        # this will result in a self-comparison, but that is OK and makes some
        # things easier in _permute_and_run
        src_list = [
            src,
        ] + [v for v in source_dict.values()]
        similarity = pycode_similar.detect(src_list)

        results: _single_result = collections.OrderedDict()
        for class_id, sim in zip(source_dict.keys(), similarity):
            results[class_id] = ResultsContainer(
                count=sim[1][0].plagiarism_count,
                total=sim[1][0].total_count,
                similarity_fraction=sim[1][0].plagiarism_percent,
                base_class=reference,
                this_class=class_id,
            )
        return results

    def _permute_and_run(
        self, source_dict: OrderedDict[int, str]
    ) -> _sim_results_tuple:
        N = len(source_dict)
        similarity_matrix = np.ones((N, N))
        results_by_ref: _nested_source_dict = {}
        sim_axis = tuple([i for i in source_dict.keys()])
        for iref, ref in enumerate(source_dict.keys()):
            results = self._compare_single_set(source_dict.copy(), ref)
            sim_array = np.array([r.similarity_fraction for r in results.values()])
            similarity_matrix[iref, :] = sim_array
            results_by_ref[ref] = results

        # correct for asymmetry
        similarity_matrix = (similarity_matrix.T + similarity_matrix) / 2.0
        return results_by_ref, similarity_matrix, sim_axis
