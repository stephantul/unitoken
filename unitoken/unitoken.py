import logging
from functools import lru_cache
from itertools import chain
from typing import List

from ftlangdetect import detect
from spacy import Language, blank

from unitoken.constants import ALLOWED_LANGUAGES


logger = logging.getLogger("unitoken")


@lru_cache
def get_blank(language: str) -> Language:
    logger.info(f"Creating {language} object.")
    nlp = blank(language)
    nlp.add_pipe("sentencizer")
    return nlp


def sent_tokenize(text: str, score_threshold: float = 0.9) -> List[List[str]]:
    detection_result = detect(text)

    language, score = detection_result["lang"], detection_result["score"]

    if score < score_threshold:
        raise ValueError(f"The score, {score}, was below threshold {score_threshold}")
    if language not in ALLOWED_LANGUAGES:
        raise ValueError(f"The detected language, {language}, was not in the set of languages.")

    blanky = get_blank(language)
    doc = blanky(text)
    return [[token.text for token in sent] for sent in doc.sents]


def tokenize(text: str, score_threshold: float = 0.9) -> List[str]:
    return list(chain(*sent_tokenize(text, score_threshold)))
