from test.data import multiline_metadata, one_line_metadata

import pytest

from app.metadata_scorer import MetaDataSimilarityScorer


@pytest.fixture(scope="module")
def scorer():
    return MetaDataSimilarityScorer()


@pytest.fixture(scope="module")
def multiline_example_scorer():
    return MetaDataSimilarityScorer(multiline=True)


@pytest.fixture
def test_oneline_metadata():
    return one_line_metadata


@pytest.fixture
def test_multiline_metadata():
    return multiline_metadata


def test_empty_query(scorer):
    result = scorer.compute_similarity_matrix({})
    assert result == {"ids": [], "matrix": []}


def test_one_query_string(scorer, test_oneline_metadata):
    test_query = {"some_id": test_oneline_metadata[0]}
    result = scorer.compute_similarity_matrix(test_query)
    assert result == {"ids": ["some_id"], "matrix": [[1.0]]}


def test_score_for_same_string_is_1(scorer, test_oneline_metadata):
    scores = scorer.compute_similarity_matrix(
        {0: test_oneline_metadata[0], 1: test_oneline_metadata[0]}
    )["matrix"]
    assert scores[0][1] == 1.0


def test_score_for_different_strings_not_1(scorer, test_oneline_metadata):
    scores = scorer.compute_similarity_matrix(
        {0: test_oneline_metadata[0], 1: test_oneline_metadata[1]}
    )["matrix"]
    assert scores[0][1] < 1.0


def test_two_similar_strings_have_high_similarity_score(
    scorer, test_oneline_metadata
):
    similar_metadata1 = test_oneline_metadata[5]
    similar_metadata2 = test_oneline_metadata[6]
    other_metadata = test_oneline_metadata[0]
    test_query = {
        "sent1": similar_metadata1,
        "sent2": similar_metadata2,
        "sent3": other_metadata,
    }
    scores = scorer.compute_similarity_matrix(test_query)["matrix"]
    assert scores[0][1] > scores[0][2]


def test_that_all_ids_from_input_returned(scorer, test_oneline_metadata):
    test_query = dict(
        zip(range(len(test_oneline_metadata)), test_oneline_metadata)
    )
    result = scorer.compute_similarity_matrix(test_query)
    assert result["ids"] == list(range(13))


def test_scores_multiple_strings(scorer, test_oneline_metadata):
    test_query = dict(
        zip(range(len(test_oneline_metadata)), test_oneline_metadata)
    )
    result = scorer.compute_similarity_matrix(test_query)["matrix"]
    eigen_scores = [result[i][i] for i in range(len(result))]
    assert eigen_scores[0] == 1
    assert pytest.approx(sum(eigen_scores)) == len(test_oneline_metadata)


def test_multiline_strings_one_example(
    multiline_example_scorer, test_multiline_metadata
):
    test_query = {"some_id": test_multiline_metadata[0]}
    result = multiline_example_scorer.compute_similarity_matrix(test_query)
    assert result == {"ids": ["some_id"], "matrix": [[1.0]]}


def test_scores_for_multiline_strings_same_string(
    multiline_example_scorer, test_multiline_metadata
):
    scores = multiline_example_scorer.compute_similarity_matrix(
        {0: test_multiline_metadata[0], 1: test_multiline_metadata[0]}
    )["matrix"]
    assert scores[0][1] == 1.0


def test_multiline_scores_for_different_strings_not_one(
    multiline_example_scorer, test_multiline_metadata
):
    scores = multiline_example_scorer.compute_similarity_matrix(
        {0: test_multiline_metadata[0], 1: test_multiline_metadata[3]}
    )["matrix"]
    assert scores[0][1] < 1.0


def test_multiline_scores_for_multiple_queries(
    multiline_example_scorer, test_multiline_metadata
):
    test_query = dict(
        zip(range(len(test_multiline_metadata)), test_multiline_metadata)
    )
    scores = multiline_example_scorer.compute_similarity_matrix(test_query)[
        "matrix"
    ]
    eigen_scores = [scores[i][i] for i in range(len(scores))]
    assert all([score == 1 for score in eigen_scores])
