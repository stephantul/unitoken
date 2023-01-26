import logging
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from itertools import repeat
from typing import Dict, List, Optional, Tuple

from ftlangdetect import detect
from spacy import Language, blank
from spacy.tokens import Doc

from unitoken.constants import SPACY_LANGUAGES

logger = logging.getLogger("unitoken")


@dataclass
class LanguageResult:
    """The score, language, and whether the language was valid"""

    score: float
    language: str
    valid: bool = True


SentencesAndLanguage = Tuple[List[List[str]], LanguageResult]
TokensAndLanguage = Tuple[List[str], LanguageResult]
DocsAndLanguage = Tuple[Doc, LanguageResult]


@lru_cache
def _get_blank(language: str) -> Language:
    """Gets a SpaCy 'blank' model, adds a sentencizer, and caches it.

    Does not support every language.

    :param language: The language of the spacy blank object.
    :return: A SpaCy blank model
    """
    logger.info(f"Creating {language} object.")
    nlp = blank(language)
    nlp.add_pipe("sentencizer")
    return nlp


def _detect_language(text: str) -> LanguageResult:
    """Detects the language of a piece of text"""
    result = detect(text)
    return LanguageResult(result["score"], result["lang"])


def _get_model(language: str, predefined_models: Dict[str, Language]) -> Language:
    """
    Gets a model for a specified language.

    If the model is not in predefined_models, a blank model is returned.

    :param language: The language of for which to return a model.
    :param predefined_models: A dictionary mapping from languages to models. Can be empty.
    :return: A model
    """
    try:
        model = predefined_models[language]
    except KeyError:
        if language not in SPACY_LANGUAGES:
            logger.error(
                f"No spacy model found for {language} and no alternative predefined model passed."
            )
            raise ValueError(f"Wrong language passed {language}.")
        model = _get_blank(language)

    return model


def _get_predefined_models(
    models: Optional[Dict[str, Language]], needs_sentence: bool
) -> Dict[str, Language]:
    """
    Turns a dictionary mapping from languages to models or None into a dictionary.

    If None is passed into this function, it returns an empty dictionary.

    :param models: None or a dictionary mapping from language to a model.
    :param needs_sentence: Whether we want models to be able to create sentences.
        We check if models have a 'sentencizer' or 'senter' component.
    :return: A possibly empty dictionary mapping from languages to models.
    :raises ValueError: if needs_sentence is True and one of the models does not have
        a 'senter' or 'sentencizer'.
    """
    if models is None:
        predefined_models = {}
    else:
        if needs_sentence:
            for language, model in models.items():
                if not set(model.component_names) & {"sentencizer", "senter"}:
                    raise ValueError(
                        f"The predefined model for {language} does not have a sentencizer component."
                    )
        predefined_models = models

    return predefined_models


def _unpack_doc_sentence(doc: Optional[Doc]) -> List[List[str]]:
    """Unpacks a doc into lists of tokens. Each sublist is a sentence"""
    if doc is None:
        return [[]]
    return [[token.text for token in sent] for sent in doc.sents]


def _unpack_doc(doc: Optional[Doc]) -> List[str]:
    """Unpacks a doc into a single list of tokens"""
    if doc is None:
        return []
    return [token.text for token in doc]


def sent_tokenize(
    text: str,
    models: Optional[Dict[str, Language]] = None,
) -> SentencesAndLanguage:
    """
    Tokenize a string into sentences.

    :param text: The text to tokenize.
    :param models: Predefined models.
    :return: A list of lists of tokens and the language classification for the item.
    """
    predefined_models = _get_predefined_models(models, True)
    doc, language_result = _base_tokenize_batch([text], predefined_models)[0]

    return _unpack_doc_sentence(doc), language_result


def tokenize(
    text: str,
    models: Optional[Dict[str, Language]] = None,
) -> TokensAndLanguage:
    """
    Tokenize a string into tokens.

    :param text: The text to tokenize.
    :param models: Predefined models.
    :return: A list of tokens and the language classification for the item.
    """
    predefined_models = _get_predefined_models(models, False)
    doc, language_result = _base_tokenize_batch([text], predefined_models)[0]

    return _unpack_doc(doc), language_result


def _base_tokenize_batch(
    texts: List[str], predefined_models: Dict[str, Language]
) -> List[DocsAndLanguage]:
    """A helper function for tokenization in batches."""
    grouped_by_language = defaultdict(list)

    for index, text in enumerate(texts):
        language_result = _detect_language(text)
        grouped_by_language[language_result.language].append(
            (index, text, language_result)
        )

    out: List[Tuple[int, Doc, LanguageResult]] = []

    for language, grouped in grouped_by_language.items():
        indices, grouped_texts, language_results = zip(*grouped)

        try:
            model = _get_model(language, predefined_models)
            docs = model.pipe(grouped_texts)
        except ValueError:
            for result in language_results:
                result.valid = False
            docs = repeat(None)

        out.extend(zip(indices, docs, language_results))

    return [
        (doc, language_result)
        for _, doc, language_result in sorted(out, key=lambda x: x[0])
    ]


def tokenize_batch(
    texts: List[str], models: Optional[Dict[str, Language]] = None
) -> List[TokensAndLanguage]:
    """
    A batched version of tokenize. Might improve performance for a large number of items.

    :param texts: A list of texts to tokenize.
    :param score_threshold: Any items below this threshold do not get parsed.
    :return: A list of tokens and the language classification for the items.
    """
    predefined_models = _get_predefined_models(models, False)
    return [
        (_unpack_doc(doc), language_result)
        for doc, language_result in _base_tokenize_batch(texts, predefined_models)
    ]


def sent_tokenize_batch(
    texts: List[str], models: Optional[Dict[str, Language]] = None
) -> List[SentencesAndLanguage]:
    """
    A batched version of sent_tokenize. Might improve performance for a large number of items.

    :param texts: A list of texts to tokenize.
    :return: A list of lists of tokens and the language classification for the items.
    """
    predefined_models = _get_predefined_models(models, True)
    return [
        (_unpack_doc_sentence(doc), language_result)
        for doc, language_result in _base_tokenize_batch(texts, predefined_models)
    ]
