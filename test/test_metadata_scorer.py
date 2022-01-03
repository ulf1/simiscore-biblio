import pytest

from app.metadata_scorer import MetaDataSimilarityScorer


@pytest.fixture(scope="module")
def scorer():
    return MetaDataSimilarityScorer()


@pytest.fixture
def test_sentences():
    return [
        "Beenken, Hermann: Das Neunzehnte Jahrhundert in der deutschen Kunst, München: Bruckmann 1944, S. 167",
        "Süddeutsche Zeitung, 1995. Zitiert nach: Süddeutsche Zeitung, 27.11.1945.",
        "Lehmann, Arthur-Heinz: Mensch, sei positiv dagegen!, Dresden: Heyne 1939 [1939], S. 96",
        "Werfel, Franz: Die Vierzig Tage des Musa Dagh I, Stockholm: Bermann - Fischer 1947 [1933], S. 225",
        "Reimann, Hans: Vergnügliches Handbuch der Deutschen Sprache, Düsseldorf: Econ-Verl. 1964 [1931], S. 212",
        "Christ, Lena: Die Rumplhanni. In: Deutsche Literatur von Frauen, Berlin: Directmedia Publ. 2001 [1917], S. 13229",
        "Christ, Lena: Die Rumplhanni. In: Deutsche Literatur von Frauen, Berlin: Directmedia Publ. 2001 [1917], S. 13247",
        "Christ, Lena: Erinnerungen einer Überflüssigen. In: Deutsche Literatur von Frauen, Berlin: Directmedia Publ. 2001 [1912], S. 12498",
        "Stadler, Arnold: Sehnsucht, Köln: DuMont Literatur und Kunst Verlag 2002, S. 102",
        "Hippel, Theodor Gottlieb von: Lebensläufe nach Aufsteigender Linie. Bd. 3,2. Berlin, 1781.",
        "Rudolphi, Caroline Christiane Louise: Gemälde weiblicher Erziehung. Bd. 1. Heidelberg, 1807.",
        "Nestroy, Johann: Einen Jux will er sich machen. Wien, 1844.",
        "Rosegger, Peter: Die Schriften des Waldschulmeisters. Pest, 1875."
        "Die Zeit, 19.10.2000, Nr. 43",
    ]
