import uuid
from typing import Dict

import datasketch
import kshingle


class MetaDataSimilarityScorer:
    def __init__(self, max_k: int = 5) -> None:
        self.max_k = max_k

    def compute_similarity_matrix(
        self, query_sents: Dict[uuid.UUID, str]
    ) -> Dict[str, list]:
        ids = []
        similarity_matrix = []
        return {"ids": ids, "matrix": similarity_matrix}
