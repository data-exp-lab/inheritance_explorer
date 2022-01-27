import abc
from typing import Any, Optional, List, Tuple, Dict, OrderedDict
import pycode_similar
import numpy as np
import collections


class ResultsContainer:
    def __init__(self, results_dict: dict):
        for ky, val in results_dict.items():
            setattr(self, ky, val)


class SimilarityContainer(abc.ABC):

    _valid_methods: List[str] = ["permute", "reference"]

    def __init__(self, method: str = "reference"):
        if method not in self._valid_methods:
            raise ValueError(
                f"Provided method not recognized, must be in {self._valid_methods}"
            )
        self.method = method
        self.results = None  # for storing results of similarity tests

    def run(self, source_dict: OrderedDict[Any, str], reference: Optional[Any] = None):
        """
        source_dict : dict
            dictionary mapping a node identifier to a source code string
        """

        source_dict_c = source_dict.copy()
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
    def _permute_and_run(self, source_dict: OrderedDict[Any, str]):
        pass

    @abc.abstractmethod
    def _compare_single_set(
        self, source_dict: OrderedDict[Any, str], reference: Any
    ) -> OrderedDict[Any, ResultsContainer]:
        pass

    # @staticmethod
    # def _expand_source_tuples(source_tuples: List[Tuple[Any, str]]) -> Tuple[List[Any], List[str]]:
    #     identifiers = [s_t[0] for s_t in source_tuples]
    #     source_codes = [s_t[1] for s_t in source_tuples]
    #     return identifiers, source_codes


class PycodeSimilarity(SimilarityContainer):
    @staticmethod
    def _validate_source_order(
        identifiers: List[Any], source_codes: List[str], reference: Any
    ) -> Tuple[List[Any], List[str]]:

        # reorder so that the reference is first
        ref_indx = identifiers.index(reference)

        if ref_indx != 0:
            # reorder so the reference is first
            new_ids = [
                identifiers[ref_indx],
            ] + identifiers[:ref_indx]
            new_src = [
                source_codes[ref_indx],
            ] + source_codes[:ref_indx]
            if ref_indx <= len(identifiers) - 1:
                new_ids += identifiers[ref_indx + 1 :]
                new_src += source_codes[ref_indx + 1 :]
            return new_ids, new_src
        return identifiers, source_codes

    def _compare_single_set(
        self, source_dict: OrderedDict[Any, str], reference: Any
    ) -> OrderedDict[Any, ResultsContainer]:
        """
        source_tuples : list
            list of two-element tuple of (node identifier, source code string)
        """

        src = source_dict[reference]  # extract the reference
        # this will result in a self-comparison, but that is OK and makes some
        # things easier in _permute_and_run
        src_list = [
            src,
        ] + [v for v in source_dict.values()]
        similarity = pycode_similar.detect(src_list)

        results = collections.OrderedDict()
        for id, sim in zip(source_dict.keys(), similarity):
            results[id] = ResultsContainer(
                {
                    "count": sim[1][0].plagiarism_count,
                    "total": sim[1][0].total_count,
                    "similarity_fraction": sim[1][0].plagiarism_percent,
                    "base_class": reference,
                    "this_class": id,
                }
            )
        return results

    def _permute_and_run(
        self, source_dict: OrderedDict[Any, str]
    ) -> Tuple[Dict, np.ndarray, tuple]:
        N = len(source_dict)
        similarity_matrix = np.ones((N, N))
        results_by_ref = {}
        sim_axis = tuple([i for i in source_dict.keys()])
        for iref, ref in enumerate(source_dict.keys()):
            results = self._compare_single_set(source_dict.copy(), ref)
            sim_array = np.array([r.similarity_fraction for r in results.values()])
            similarity_matrix[iref, :] = sim_array
            results_by_ref[ref] = results
        return results_by_ref, similarity_matrix, sim_axis
