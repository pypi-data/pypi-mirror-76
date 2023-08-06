import re


class BaseCleaner():
    def __init__(self, *args, **kwargs):
        self.re_match = None
        self.sub = " "

    def run(self, text):
        cleaned_text = self.re_match.sub(self.sub, text)
        return cleaned_text

    def configuration(self):
        return self.__dict__


class CommentsCleaner(BaseCleaner):
    def __init__(self, sub=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.re_match = re.compile(r"""(\"[^\"]*\"(?!\\))|(//[^\n]*$|/(?!\\)\*[\s\S]*?\*(?!\\)/)""")
        self.sub = sub if sub else " "


class CopyrightCleaner(CommentsCleaner):
    def __init__(self, sub=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.license_keywords = re.compile("(copyright|license|licensed)", re.IGNORECASE)
        self.sub = sub if sub else " "

    def run(self, text):
        matches = self.re_match.findall(text)
        for _, matched in matches:
            if self.license_keywords.findall(matched):
                text = text.replace(matched, self.sub)

        return text


class DigitsCleaner(BaseCleaner):
    """
    Clean numbers
    """

    def __init__(self, sub=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.re_match = re.compile(r"""\b\d+\b""")
        self.sub = sub if sub else " "


class KeywordsCleaner(BaseCleaner):
    """
    Clean language keywords from the text
    """

    def __init__(self, language="java", *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open(f"resources/{language}/keywords.txt", "rt", encoding="utf8") as inf:
            words = set(inf.readlines())

        pattern = []
        for word in words:
            word = word.strip()
            pattern.append(r"\b" + word.strip() + r"\b")

        pattern = "(" + "|".join(pattern) + ")"
        self.re_match = re.compile(pattern, re.IGNORECASE)
