import uuid
from typing import Dict, List, Set

import datasketch
import kshingle as ks
from bs4 import BeautifulSoup


class MetaDataSimilarityScorer:
    """
    Computes similarity scores for bibliographic information based on
    k-shingle of strings. Default maximal k for shingling is 5.

    Query strings should either all be in one-line format or strings of
    tagged xml-data:
    1. One-line example:
        Rosegger, Peter: Die Schriften des Waldschulmeisters. Pest, 1875.

    2. Multi-line example:
        <Beleg>
          <Belegtext>
            Ramazan Yildirim meinte in der Pressekonferenz nach dem Spiel, dass
             sein bereits umspielter <Stichwort>Torwart</Stichwort> Thomas
             Kraus nicht berührt habe.
          </Belegtext>
          <Fundstelle>
            <Dokument>tb/tbdTDb7V</Dokument>
            <Korpus>blogs</Korpus>
            <Autor>Veröffentlicht</Autor>
            <Titel>Fortuna Köln - Sportfreunde Lotte 1-2 (1-2)</Titel>
            <Textklasse>internetbasiert</Textklasse>
            <Bibl>Fortuna Köln - Sportfreunde Lotte 1-2 (1-2). The Boy In The
                Bubble, 2013-10-06</Bibl>
            <URL>http://surfguard.wordpress.com/2013/10/06/fortuna-koln-
            sportfreunde-lotte-1-2/</URL>
            <Datum>06.10.2013</Datum>
            <Aufrufdatum>21.07.2020</Aufrufdatum>
          </Fundstelle>
        </Beleg>

    For the computation of similarity scores for multi-line examples, as
    default only the part between the <Fundstelle> tag will be considered.
    """

    def __init__(
        self,
        max_k: int = 5,
        num_perm: int = 256,
        multiline: bool = False,
        start_tag: str = "fundstelle",
    ) -> None:
        """
        Args:
            max_k: int
                    Maximal character length for shingles. Default is 5

            multiline: bool
                    Type of query strings. Use True, if queries are multi-line
                    strings. Default is False.

            start_tag: str
                    Tag for xml-multi-line query strings to denote the parts of
                    the xml data to use. Default is 'fundstelle'

        """
        self.max_k = max_k
        self.num_perm = num_perm
        self.multiline = multiline
        self.start_tag = start_tag

    def compute_similarity_matrix(
        self, query_sents: Dict[uuid.UUID, str]
    ) -> Dict[str, list]:
        """
        Compute similarity scores for bibliographic meta-information.

        query_sents: Dict[uuid.UUID, str]
            A dictionary where keys are UUIDs and values are the strings to
            process.

        Returns: Dict[str, list]
            A dictionary with the keys 'ids' (storing the query ids as a list)
            and 'matrix' (the matrix of similarity scores).
            The list of IDs and the position in the matrix are index-assorted.
        """
        ids = list(query_sents.keys())
        minhash_table = self._fill_minhash_table(list(query_sents.values()))
        similarity_matrix = [
            [
                minhash_table[i].jaccard(minhash_table[j])
                for j in range(len(minhash_table))
            ]
            for i in range(len(minhash_table))
        ]
        return {"ids": ids, "matrix": similarity_matrix}

    def _fill_minhash_table(
        self, query_sents: List[str]
    ) -> List[datasketch.MinHash]:
        minhash_table = []
        if self.multiline:
            query_sents = [
                self._remove_tags_from_multiline_strings(example)
                for example in query_sents
            ]
        for sentence in query_sents:
            shingle_set = ks.shingleset_k(sentence, self.max_k)
            minhash = self._hash_shingle_set(shingle_set)
            minhash_table.append(minhash)
        return minhash_table

    def _hash_shingle_set(self, shingle_set: Set[str]) -> datasketch.MinHash:
        minhash = datasketch.MinHash(num_perm=self.num_perm)
        for shingle in shingle_set:
            minhash.update(shingle.encode("utf-8"))
        return minhash

    def _remove_tags_from_multiline_strings(
        self, multi_line_example: str
    ) -> str:
        example_soup = BeautifulSoup(
            multi_line_example, features="html.parser"
        )
        return " ".join(
            [tag.text for tag in example_soup.find(self.start_tag)]
        )
