import uuid
from typing import Dict, List, Set
from bs4 import BeautifulSoup
import datasketch
import kshingle


class MetaDataSimilarityScorer:
    def __init__(self, max_k: int = 5, multiline=False) -> None:
        self.max_k = max_k
        self.multiline = multiline

    def compute_similarity_matrix(
        self, query_sents: Dict[uuid.UUID, str]
    ) -> Dict[str, list]:
        ids = list(query_sents.keys())
        minhash_table = self._fill_minhash_table(query_sents.values())
        similarity_matrix = [
            [
                minhash_table[i].jaccard(minhash_table[j])
                for j in range(len(minhash_table))
            ]
            for i in range(len(minhash_table))
        ]
        return {"ids": ids, "matrix": similarity_matrix}

    def _fill_minhash_table(self, query_sents: List[str]) -> List[datasketch.MinHash]:
        minhash_table = []
        if self.multiline:
            query_sents = [
                self._remove_tags_from_multiline_strings(example)
                for example in query_sents
            ]
        for sentence in query_sents:
            shingle_set = kshingle.shingleset_k(sentence, self.max_k)
            minhash = self._hash_shingle_set(shingle_set)
            minhash_table.append(minhash)
        return minhash_table

    def _hash_shingle_set(self, shingle_set: Set[str]) -> datasketch.MinHash:
        minhash = datasketch.MinHash(num_perm=256)
        for shingle in shingle_set:
            minhash.update(shingle.encode("utf-8"))
        return minhash

    def _remove_tags_from_multiline_strings(self, multi_line_example: str):
        multi_line_example = BeautifulSoup(multi_line_example, features="html.parser")
        return " ".join([tag.text for tag in multi_line_example.find("fundstelle")])
