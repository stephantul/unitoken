import logging
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Optional, Tuple

from ftlangdetect import detect
from spacy import Language, blank
from spacy.tokens import Doc

from unitoken.constants import ALLOWED_LANGUAGES

logger = logging.getLogger("unitoken")


@dataclass
class LanguageResult:
    score: float
    language: str


SentencesAndLanguage = Tuple[List[List[str]], LanguageResult]
TokensAndLanguage = Tuple[List[str], LanguageResult]
DocsAndLanguage = Tuple[Doc, LanguageResult]


@lru_cache
def _get_blank(language: str) -> Language:
    logger.info(f"Creating {language} object.")
    nlp = blank(language)
    nlp.add_pipe("sentencizer")
    return nlp


def _detect_language(text: str) -> LanguageResult:
    result = detect(text)
    return LanguageResult(result["score"], result["lang"])


def _get_model(language: str, predefined_models: Dict[str, Language]) -> Language:
    try:
        model = predefined_models[language]
    except KeyError:
        model = _get_blank(language)

    return model


def _get_predefined_models(
    models: Optional[Dict[str, Language]], needs_sentence: bool
) -> Dict[str, Language]:
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


def _unpack_doc_sentence(doc: Doc) -> List[List[str]]:
    return [[token.text for token in sent] for sent in doc.sents]


def _unpack_doc(doc: Doc) -> List[str]:
    return [token.text for token in doc]


def _base_tokenize(
    text: str, score_threshold: float, predefined_models: Dict[str, Language]
) -> Tuple[Doc, LanguageResult]:
    language_result = _detect_language(text)
    language, score = language_result.language, language_result.score

    if score < score_threshold:
        raise ValueError(f"The score, {score}, was below threshold {score_threshold}")
    if language not in ALLOWED_LANGUAGES | set(predefined_models):
        raise ValueError(
            f"The detected language, {language}, was not in the set of languages."
        )

    model = _get_model(language, predefined_models)
    return model(text), language_result


def sent_tokenize(
    text: str,
    score_threshold: float = 0.9,
    models: Optional[Dict[str, Language]] = None,
) -> SentencesAndLanguage:
    predefined_models = _get_predefined_models(models, True)
    doc, language_result = _base_tokenize(text, score_threshold, predefined_models)

    return [[token.text for token in sent] for sent in doc.sents], language_result


def tokenize(
    text: str,
    score_threshold: float = 0.9,
    models: Optional[Dict[str, Language]] = None,
) -> TokensAndLanguage:
    predefined_models = _get_predefined_models(models, False)
    doc, language_result = _base_tokenize(text, score_threshold, predefined_models)

    return [token.text for token in doc], language_result


def _base_tokenize_batch(
    texts: List[str], predefined_models: Dict[str, Language]
) -> List[DocsAndLanguage]:
    grouped_by_language = defaultdict(list)

    for index, text in enumerate(texts):
        language_result = _detect_language(text)
        grouped_by_language[language_result.language].append(
            (index, text, language_result)
        )

    out: List[Tuple[int, Doc, LanguageResult]] = []

    for language, grouped in grouped_by_language.items():
        indices, grouped_texts, language_results = zip(*grouped)

        model = _get_model(language, predefined_models)
        docs = model.pipe(grouped_texts)
        out.extend(zip(indices, docs, language_results))

    return [
        (doc, language_result)
        for _, doc, language_result in sorted(out, key=lambda x: x[0])
    ]


def tokenize_batch(
    texts: List[str], models: Optional[Dict[str, Language]] = None
) -> List[TokensAndLanguage]:
    predefined_models = _get_predefined_models(models, False)
    return [
        (_unpack_doc(doc), language_result)
        for doc, language_result in _base_tokenize_batch(texts, predefined_models)
    ]


def sent_tokenize_batch(
    texts: List[str], models: Optional[Dict[str, Language]] = None
) -> List[SentencesAndLanguage]:
    predefined_models = _get_predefined_models(models, True)
    return [
        (_unpack_doc_sentence(doc), language_result)
        for doc, language_result in _base_tokenize_batch(texts, predefined_models)
    ]
