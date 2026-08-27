import re

from normalizer import TextNormalizer


class ProductExtractor:

    @staticmethod
    def detect_region(row):
        text = TextNormalizer.normalize(
            f"{row.get('region_lock', '')} "
            f"{row.get('region_notes', '')} "
            f"{row.get('country', '')} "
            f"{row.get('clean_name', '')}"
        )

        if (
            "global" in text
            or "worldwide" in text
            or "region free" in text
        ):
            return "GLOBAL"

        if (
            "north america" in text
            or "united states" in text
            or " usa " in f" {text} "
        ):
            return "NA"

        if (
            "europe" in text
            or "european union" in text
        ):
            return "EU"

        if "poland" in text:
            return "PL"

        if (
            "united kingdom" in text
            or "great britain" in text
        ):
            return "UK"

        if "turkey" in text:
            return "TR"

        return ""

    @staticmethod
    def detect_platform(row):
        text = TextNormalizer.normalize(
            f"{row.get('clean_name', '')} "
            f"{row.get('original_name', '')} "
            f"{row.get('drm', '')}"
        )

        patterns = [
            (
                "PLAYSTATION",
                [
                    "playstation",
                    "psn",
                    "ps4",
                    "ps5",
                ]
            ),

            (
                "XBOX",
                [
                    "xbox",
                    "microsoft store",
                    "xbox live",
                ]
            ),

            (
                "NINTENDO",
                [
                    "nintendo",
                    "switch",
                    "eshop",
                ]
            ),

            (
                "STEAM",
                [
                    "steam",
                ]
            ),

            (
                "EPIC",
                [
                    "epic games",
                ]
            ),

            (
                "BATTLE_NET",
                [
                    "battle.net",
                    "battle net",
                ]
            ),

            (
                "PC",
                [
                    "(pc)",
                    " pc ",
                ]
            ),
        ]

        padded = f" {text} "

        for platform, words in patterns:
            for word in words:
                if word in padded:
                    return platform

        return ""

    @staticmethod
    def extract_money_value(text):
        text = TextNormalizer.normalize(
            text
        )

        currencies = (
            "pln|eur|usd|gbp|aud|cad|"
            "brl|try|jpy|sek|nok|dkk|"
            "chf|nzd|mxn"
        )

        patterns = [
            rf"\b(\d+(?:[.,]\d+)?)\s*({currencies})\b",

            rf"\b({currencies})\s*(\d+(?:[.,]\d+)?)\b",

            r"\$(\d+(?:[.,]\d+)?)",

            r"€(\d+(?:[.,]\d+)?)",

            r"£(\d+(?:[.,]\d+)?)",
        ]

        for i, pattern in enumerate(
            patterns
        ):
            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if not match:
                continue

            if i == 0:
                return (
                    match.group(1).replace(
                        ",",
                        "."
                    ),
                    match.group(2).upper()
                )

            if i == 1:
                return (
                    match.group(2).replace(
                        ",",
                        "."
                    ),
                    match.group(1).upper()
                )

            if i == 2:
                return (
                    match.group(1).replace(
                        ",",
                        "."
                    ),
                    "USD"
                )

            if i == 3:
                return (
                    match.group(1).replace(
                        ",",
                        "."
                    ),
                    "EUR"
                )

            if i == 4:
                return (
                    match.group(1).replace(
                        ",",
                        "."
                    ),
                    "GBP"
                )

        return "", ""

    @staticmethod
    def extract_duration(text):
        text = TextNormalizer.normalize(
            text
        )

        match = re.search(
            r"\b(\d+)\s*"
            r"(day|days|month|months|year|years)\b",
            text
        )

        if not match:
            return ""

        number = match.group(1)
        unit = match.group(2)

        if unit.startswith("day"):
            return f"{number}D"

        if unit.startswith("month"):
            return f"{number}M"

        if unit.startswith("year"):
            return f"{number}Y"

        return ""

    @staticmethod
    def extract_devices(text):
        text = TextNormalizer.normalize(
            text
        )

        match = re.search(
            r"\b(\d+)\s*devices?\b",
            text
        )

        if match:
            return match.group(1)

        return ""

    @staticmethod
    def extract_quantity(
        text,
        unit_words
    ):
        text = TextNormalizer.normalize(
            text
        )

        units = "|".join(
            re.escape(word)
            for word in unit_words
        )

        match = re.search(
            rf"\b(\d[\d\s.,]*)\s*(?:{units})\b",
            text
        )

        if not match:
            return ""

        value = match.group(1)

        value = value.replace(
            " ",
            ""
        )

        value = value.replace(
            ",",
            ""
        )

        return value