import logging
from dataclasses import dataclass
from functools import lru_cache
from itertools import chain
from typing import Dict, List, Optional, Tuple

from ftlangdetect import detect
from spacy import Language, blank

from unitoken.constants import ALLOWED_LANGUAGES

logger = logging.getLogger("unitoken")


@dataclass
class LanguageResult:
    score: float
    language: str


@lru_cache
def get_blank(language: str) -> Language:
    logger.info(f"Creating {language} object.")
    nlp = blank(language)
    nlp.add_pipe("sentencizer")
    return nlp


def detect_language(text: str) -> LanguageResult:
    result = detect(text)
    return LanguageResult(result["score"], result["lang"])


def sent_tokenize(
    text: str,
    score_threshold: float = 0.9,
    models: Optional[Dict[str, Language]] = None,
) -> Tuple[List[List[str]], LanguageResult]:
    if models is None:
        predefined_models = {}
    else:
        predefined_models = models

    language_result = detect_language(text)
    language, score = language_result.language, language_result.score

    if score < score_threshold:
        raise ValueError(f"The score, {score}, was below threshold {score_threshold}")
    if language not in ALLOWED_LANGUAGES | set(predefined_models):
        raise ValueError(
            f"The detected language, {language}, was not in the set of languages."
        )

    try:
        model = predefined_models[language]
    except KeyError:
        model = get_blank(language)

    doc = model(text)

    return [[token.text for token in sent] for sent in doc.sents], language_result


def tokenize(
    text: str,
    score_threshold: float = 0.9,
    models: Optional[Dict[str, Language]] = None,
) -> Tuple[List[str], LanguageResult]:
    sentences, language_result = sent_tokenize(text, score_threshold, models)
    return list(chain(*sentences)), language_result
