import abc
from typing import Any, Optional, List, Tuple
import pycode_similar
import numpy as np

class ResultsContainer:
    def __init__(self, results_dict: dict):
        for ky, val in results_dict.items():
            setattr(self, ky, val)


class SimilarityContainer(abc.ABC):

    _valid_methods: List[str] = ["permute", "reference"]

    def __init__(self, method: str = "reference"):
        if method not in self._valid_methods :
            raise ValueError(f"Provided method not recognized, must be in {self._valid_methods}")
        self.method = method
        self.results = None  # for storing results of similarity tests

    def run(self, source_tuples: List[Tuple[Any, str]], reference: Optional[Any] = None):
        """
        source_tuples : list
            list of two-element tuple of (node identifier, source code string)
        """

        if self.method == "permute":
            self.results = self._permute_and_run(source_tuples)
        else:
            if reference not in [s_t[0] for s_t in source_tuples] or reference is None:
                raise ValueError("The value for the reference parameter is not in the source_tuples list")
            self.results = self._compare_single_set(source_tuples, reference)

    @abc.abstractmethod
    def _permute_and_run(self, source_tuples: List[Tuple[Any, str]]):
        """
        source_tuples : list
            list of two-element tuple of (node identifier, source code string)
        """
        pass


    @abc.abstractmethod
    def _compare_single_set(self, source_tuples: List[Tuple[Any, str]], reference: Any):
        """
        source_tuples : list
            list of two-element tuple of (node identifier, source code string)
        """
        pass

    @staticmethod
    def _expand_source_tuples(source_tuples: List[Tuple[Any, str]]) -> Tuple[List[Any], List[str]]:
        identifiers = [s_t[0] for s_t in source_tuples]
        source_codes = [s_t[1] for s_t in source_tuples]
        return identifiers, source_codes


class PycodeSimilarity(SimilarityContainer):

    @staticmethod
    def _validate_source_order(identifiers: List[Any], source_codes: List[str], reference: Any) -> Tuple[List[Any], List[str]]:

        # reorder so that the reference is first
        ref_indx = identifiers.index(reference)

        if ref_indx != 0:
            # reorder so the reference is first
            new_ids = [identifiers[ref_indx], ] + identifiers[:ref_indx]
            new_src = [source_codes[ref_indx], ] + source_codes[:ref_indx]
            if ref_indx <= len(identifiers) - 1:
                new_ids += identifiers[ref_indx + 1:]
                new_src += source_codes[ref_indx + 1:]
            return new_ids, new_src
        return identifiers, source_codes

    def _compare_single_set(self, source_tuples: List[Tuple[Any, str]], reference: Any):
        """
        source_tuples : list
            list of two-element tuple of (node identifier, source code string)
        """

        ids, srcs = self._expand_source_tuples(source_tuples)
        ids, srcs = self._validate_source_order(ids, srcs, reference)

        similarity = pycode_similar.detect(srcs)

        results = {}
        similarity_array = np.ones((len(ids),))
        id_array = np.array([int(i.replace("_", "")) for i in ids])
        for id, sim in zip(ids[1:], similarity):
            results[id] = ResultsContainer({
                           "count": sim[1][0].plagiarism_count,
                           "total": sim[1][0].total_count,
                           "similarity_fraction": sim[1][0].plagiarism_percent,
                           "base_class": reference,
                           "this_class": id,
                           })
            id_int = int(id.replace("_", "")) - 1
            similarity_array[id_array == id_int] = sim[1][0].plagiarism_percent

        results["similarity_array"] = similarity_array
        results["id_array"] = id_array
        return ResultsContainer(results)

    def _permute_and_run(self, source_tuples: List[Tuple[Any, str]]):
        """
        source_tuples : list
            list of two-element tuple of (node identifier, source code string)
        """

        ids, srcs = self._expand_source_tuples(source_tuples)

        similarity_matrix = np.ones((len(ids), len(ids)))

        for ref in ids:
            # run for every id as the reference
            results = self._compare_single_set(source_tuples, ref)
            this_row = int(ref.replace("_", "")) - 1
            similarity_matrix[this_row, results.id_array] = results.similarity_array

        return similarity_matrix


#
# import itertools
#
#
# def get_source_code(clss, f: str):
#     return textwrap.dedent(inspect.getsource(getattr(clss, f)))
#
#
# fname = "_read_particle_selection"
# f_sources = {}
# for clss in (BaseIOHandler, BaseParticleIOHandler, IOHandlerGadgetFOFHaloHDF5):
#     src = get_source_code(clss, fname)
#     f_sources[clss.__name__] = src
#
#
# def get_results(perm_keys, similarity_results):
#     result = []
#     for isim, sim in enumerate(similarity_results):
#         result.append({"count": sim[1][0].plagiarism_count,
#                        "total": sim[1][0].total_count,
#                        "frac": sim[1][0].plagiarism_percent,
#                        "base_class": perm_keys[0],
#                        "this_class": perm_keys[isim + 1],
#                        })
#     return result
#
#
# for perm in itertools.permutations(f_sources.keys()):
#     print("\nnew permutation:")
#     ordered_src = [f_sources[clss] for clss in perm]
#     sims = pycode_similar.detect(ordered_src)
#     print(get_results(perm, sims))
#
