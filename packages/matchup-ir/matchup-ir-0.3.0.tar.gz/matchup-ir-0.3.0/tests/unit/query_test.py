import unittest

from matchup.presentation.text import Term
from matchup.structure.query import Query
from matchup.structure.vocabulary import Vocabulary


class QueryTest(unittest.TestCase):
    def setUp(self):
        vocabulary = Vocabulary("./tests/static/files", stopwords="./tests/static/pt-br.txt")
        vocabulary.import_collection()

        self._query = Query(vocabulary=vocabulary)

    def test_ask(self):
        answer = 'eu sou o marcos\ntop de linha'
        processed = [Term("marcos", "1-9"), Term("top", "2-0"), Term("linha", "2-7")]

        self._query.ask(answer=answer)
        self.assertEqual(self._query.search_input, processed)
