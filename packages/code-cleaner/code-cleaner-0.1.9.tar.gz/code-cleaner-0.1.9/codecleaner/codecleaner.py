"""Main module."""
from codecleaner.cleaner import DigitsCleaner, KeywordsCleaner
from codecleaner.pipeline import Pipeline


def get_cleaner(
        clean_keywords=True,
        clean_digits=True,
        clean_strings=True,
        replace_digits_with="<NUM>",
        replace_strings_with="<STRING>",
        lang="java"):
    callables = []

    if clean_digits:
        callables.append(DigitsCleaner(replace_digits_with))

    if clean_keywords:
        callables.append(KeywordsCleaner(lang))

    return Pipeline(callables)


def get_tokenize(text):
    pass
