import uuid
from typing import Dict, List, Union

from fastapi import FastAPI

from app.metadata_scorer import MetaDataSimilarityScorer

srvurl = ""


app = FastAPI(
    title="simiscore-legal ML API",
    descriptions=(
        "ML API to compute similarity scores using bibliographic "
        "meta-information"
    ),
    version="0.1.0",
    openapi_url=f"{srvurl}/openapi.json",
    docs_url=f"{srvurl}/docs",
    redoc_url=f"{srvurl}/redoc",
)

similarity_scorer = MetaDataSimilarityScorer()


@app.get(f"{srvurl}/")
def get_info() -> dict:
    """Returns basic information about the application"""
    return {
        "version": app.version,
        "metadata_scorer": [
            f"max_k: {similarity_scorer.max_k}",
            f"multiline: {similarity_scorer.multiline}",
            f"start_tag: {similarity_scorer.start_tag}",
        ],
    }


@app.post(f"{srvurl}/similarities/", response_model=Dict[str, list])
async def compute_similarites(
    query_sents: Union[List[str], Dict[uuid.UUID, str]],
) -> Dict[str, list]:
    """
    Computes similarity score for a sequence of bibliographic strings.

    Parameters:
        query_sents: Union[dict, list]
            Sequence of strings to be processed.
    Returns: Dict[str, list]
            A dictionary containing the string ids ('ids') and a matrix
            with the similarity scores ('matrix'). Indices in the matrix
            correspond to the indices in the ids-list.
            If only a list of strings was passed, id will be created.
    """
    if isinstance(query_sents, list):
        query_sents = {uuid.uuid4(): sentence for sentence in query_sents}
    return similarity_scorer.compute_similarity_matrix(query_sents)
