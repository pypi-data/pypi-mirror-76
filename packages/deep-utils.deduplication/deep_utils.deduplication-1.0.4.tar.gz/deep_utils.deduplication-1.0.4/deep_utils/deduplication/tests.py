import unittest

from utils.document_deduplication.utils import remove_puncs_and_extra_spaces
from utils.document_deduplication.vector_generator import (
    create_count_vector,
    normalize_count_vector,
    create_trigram_vector,
    EN_TRIGRAMS,
    ES_TRIGRAMS,
    FR_TRIGRAMS,
    InvalidText,
    InvalidLanguage,
    TrigramsNotLoaded,
)

VECTOR_SIZE = 10000


def test_remove_puncs_and_extra_spaces():
    pairs = [
        ('with.punctu!!ation$$', 'with punctu ation'),
        ('$!@#another punctuated te&&xt', 'another punctuated te xt'),
        ('multiple spaces   and  space at the end ', 'multiple spaces and space at the end'),
        ('Mix^^ of CA~`SEs!!', 'mix of ca ses'),
    ]
    for txt, processed in pairs:
        assert remove_puncs_and_extra_spaces(txt) == processed


def test_trigrams_count():
    assert len(EN_TRIGRAMS.keys()) == VECTOR_SIZE, f"{VECTOR_SIZE} trigrams for english"
    assert len(ES_TRIGRAMS.keys()) == VECTOR_SIZE, f"{VECTOR_SIZE} trigrams for spanish"
    assert len(FR_TRIGRAMS.keys()) == VECTOR_SIZE, f"{VECTOR_SIZE} trigrams for french"


class TestVectorCreation(unittest.TestCase):
    """Tests for vector generation"""

    def test_count_vector(self):
        custom_trigrams = {' ab': 0, 'abc': 1, ' bc': 2, 'bc ': 3, ' is': 4, 'is ': 5}
        text = 'Abc is abc. is ab'
        # positions for [' ab', 'abc', ' bc', 'bc ', ' is', 'is ']
        expected_count_vector = [2, 2, 0, 2, 2, 2]
        processed_text = remove_puncs_and_extra_spaces(text)
        vector = create_count_vector(processed_text, custom_trigrams)
        assert len(vector) == len(custom_trigrams.values())
        assert expected_count_vector == vector

    def test_normalize_count_vector(self):
        vector = [1, 2, 3, 4, 5, 5]
        expected_normalized = [0.05, 0.1, 0.15, 0.2, 0.25, 0.25]
        assert normalize_count_vector(vector) == expected_normalized

    def test_create_trigram_vector_invalid_lang(self):
        with self.assertRaises(InvalidLanguage):
            create_trigram_vector('ch', 'test text. does not matter')

    def test_create_trigram_vector_small_document(self):
        with self.assertRaises(InvalidText):
            create_trigram_vector('en', 'te')

        with self.assertRaises(InvalidText):
            create_trigram_vector('fr', '   . ')

        with self.assertRaises(InvalidText):
            create_trigram_vector('es', None)

    def test_create_trigram_vector(self):
        # NOTE: it's infeasible to check exactly the vectors generated
        text = 'Document deduplication for Humanitarian organization!!'
        vector = create_trigram_vector('en', text)
        assert len(vector) == VECTOR_SIZE, f"There should be {VECTOR_SIZE} dimensions"

        assert all(x <= 1 for x in vector), "Every dimension should be <= 1"
        assert any(x > 0 for x in vector), "Some dimension should be > 0"
