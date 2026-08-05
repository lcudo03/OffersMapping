import re
import unicodedata

import pandas as pd


class TextNormalizer:

    @staticmethod
    def normalize(text):
        if text is None or pd.isna(text):
            return ""

        text = str(text).lower().strip()

        text = unicodedata.normalize("NFKD", text)
        text = "".join(
            c for c in text
            if not unicodedata.combining(c)
        )

        text = text.replace("–", "-")
        text = text.replace("—", "-")

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @staticmethod
    def slugify(text):
        text = TextNormalizer.normalize(text)

        text = re.sub(
            r"[^a-z0-9]+",
            "-",
            text
        )

        return text.strip("-")

    @staticmethod
    def clean_product_name(text):
        text = TextNormalizer.normalize(text)

        expressions = [
            r"\bglobal\b",
            r"\bnorth america\b",
            r"\beurope\b",
            r"\beu\b",
            r"\bregion free\b",
            r"\bcd key\b",
            r"\bkey\b",
            r"\bplayer trade\b"
        ]

        for expression in expressions:
            text = re.sub(
                expression,
                " ",
                text
            )

        text = re.sub(
            r"\s*-\s*$",
            "",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip(" -")