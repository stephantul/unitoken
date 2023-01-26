import unittest
from unitoken import tokenize, sent_tokenize


class TestUnitoken(unittest.TestCase):
    def test_tokenize_empty(self) -> None:
        empty = ""

        result, _ = sent_tokenize(empty)
        self.assertEqual(result, [])

    def test_tokenize(self) -> None:
        my_string = "de de de de de de"

        result, _ = tokenize(my_string)
        self.assertEqual(result, my_string.split())

    def test_roundtrip(self) -> None:
        my_string = "the dog walked home, and ate nice cookies down by the bay."

        tokenize_result, _ = tokenize(my_string)
        sent_tokenize_result, _ = sent_tokenize(my_string)
        self.assertEqual(sum(sent_tokenize_result, []), tokenize_result)
