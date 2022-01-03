import pytest

from app.metadata_scorer import MetaDataSimilarityScorer


@pytest.fixture(scope="module")
def scorer():
    return MetaDataSimilarityScorer()


@pytest.fixture
def test_metadata():
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


def test_empty_query(scorer):
    result = scorer.compute_similarity_matrix({})
    assert result == {"ids": [], "matrix": []}


def test_one_query_string(scorer, test_metadata):
    test_query = {"some_id": test_metadata[0]}
    result = scorer.compute_similarity_matrix(test_query)
    assert result == {"ids": ["some_id"], "matrix": [[1.0]]}


def test_score_for_same_string_is_1(scorer, test_metadata):
    scores = scorer.compute_similarity_matrix(
        {0: test_metadata[0], 1: test_metadata[0]}
    )["matrix"]
    assert scores[0][1] == 1.0


def test_score_for_different_strings_not_1(scorer, test_metadata):
    scores = scorer.compute_similarity_matrix(
        {0: test_metadata[0], 1: test_metadata[1]}
    )["matrix"]
    assert scores[0][1] < 1.0


def test_two_similar_strings_have_high_similarity_score(scorer, test_metadata):
    similar_metadata1 = test_metadata[5]
    similar_metadata2 = test_metadata[6]
    other_metadata = test_metadata[0]
    test_query = {
        "sent1": similar_metadata1,
        "sent2": similar_metadata2,
        "sent3": other_metadata,
    }
    scores = scorer.compute_similarity_matrix(test_query)["matrix"]
    assert scores[0][1] > scores[0][2]


def test_that_all_ids_from_input_returned(scorer, test_metadata):
    test_query = dict(zip(range(len(test_metadata)), test_metadata))
    result = scorer.compute_similarity_matrix(test_query)
    assert result["ids"] == list(range(13))


def test_scores_multiple_strings(scorer, test_metadata):
    test_query = dict(zip(range(len(test_metadata)), test_metadata))
    result = scorer.compute_similarity_matrix(test_query)["matrix"]
    eigen_scores = [result[i][i] for i in range(len(result))]
    assert eigen_scores[0] == 1
    assert pytest.approx(sum(eigen_scores) == len(test_metadata))
