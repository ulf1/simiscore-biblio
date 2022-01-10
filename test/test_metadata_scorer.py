import pytest
import os


from app.metadata_scorer import MetaDataSimilarityScorer


@pytest.fixture(scope="module")
def scorer():
    return MetaDataSimilarityScorer()


@pytest.fixture(scope="module")
def multiline_example_scorer():
    return MetaDataSimilarityScorer(multiline=True)


@pytest.fixture
def test_oneline_metadata():
    return [
        "Beenken, Hermann: Das Neunzehnte Jahrhundert in der deutschen Kunst, "
        "München: Bruckmann 1944, S. 167",
        "Süddeutsche Zeitung, 1995. Zitiert nach: Süddeutsche Zeitung, " "27.11.1945.",
        "Lehmann, Arthur-Heinz: Mensch, sei positiv dagegen!, Dresden: Heyne "
        "1939 [1939], S. 96",
        "Werfel, Franz: Die Vierzig Tage des Musa Dagh I, Stockholm: Bermann -"
        " Fischer 1947 [1933], S. 225",
        "Reimann, Hans: Vergnügliches Handbuch der Deutschen Sprache, "
        "Düsseldorf: Econ-Verl. 1964 [1931], S. 212",
        "Christ, Lena: Die Rumplhanni. In: Deutsche Literatur von Frauen, "
        "Berlin: Directmedia Publ. 2001 [1917], S. 13229",
        "Christ, Lena: Die Rumplhanni. In: Deutsche Literatur von Frauen, "
        "Berlin: Directmedia Publ. 2001 [1917], S. 13247",
        "Christ, Lena: Erinnerungen einer Überflüssigen. In: Deutsche Liter"
        "atur von Frauen, Berlin: Directmedia Publ. 2001 [1912], S. 12498",
        "Stadler, Arnold: Sehnsucht, Köln: DuMont Literatur und Kunst Verlag "
        "2002, S. 102",
        "Hippel, Theodor Gottlieb von: Lebensläufe nach Aufsteigender Linie. "
        "Bd. 3,2. Berlin, 1781.",
        "Rudolphi, Caroline Christiane Louise: Gemälde weiblicher Erziehung. "
        "Bd. 1. Heidelberg, 1807.",
        "Nestroy, Johann: Einen Jux will er sich machen. Wien, 1844.",
        "Rosegger, Peter: Die Schriften des Waldschulmeisters. Pest, 1875."
        "Die Zeit, 19.10.2000, Nr. 43",
    ]


@pytest.fixture
def test_multiline_metadata():
    filepath = os.path.join("test", "metadata.txt")
    with open(filepath, "r", encoding="utf-8") as ptr:
        metadata_lines = ptr.readlines()
    grouped_metadata = []
    collected = ""
    for line in metadata_lines:
        if line == "\n":
            if collected:
                grouped_metadata.append(collected)
                collected = ""
        else:
            collected += line
    else:
        grouped_metadata.append(collected)
    return grouped_metadata


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


def test_two_similar_strings_have_high_similarity_score(scorer, test_oneline_metadata):
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
    test_query = dict(zip(range(len(test_oneline_metadata)), test_oneline_metadata))
    result = scorer.compute_similarity_matrix(test_query)
    assert result["ids"] == list(range(13))


def test_scores_multiple_strings(scorer, test_oneline_metadata):
    test_query = dict(zip(range(len(test_oneline_metadata)), test_oneline_metadata))
    result = scorer.compute_similarity_matrix(test_query)["matrix"]
    eigen_scores = [result[i][i] for i in range(len(result))]
    assert eigen_scores[0] == 1
    assert pytest.approx(sum(eigen_scores) == len(test_oneline_metadata))


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
    test_query = dict(zip(range(len(test_multiline_metadata)), test_multiline_metadata))
    scores = multiline_example_scorer.compute_similarity_matrix(test_query)["matrix"]
    eigen_scores = [scores[i][i] for i in range(len(scores))]
    assert all([score == 1 for score in eigen_scores])
