import re

from normalizer import TextNormalizer


class ProductExtractor:

    CURRENCY_ALIASES = {
        "PLN": "PLN",
        "EUR": "EUR",
        "USD": "USD",
        "GBP": "GBP",
        "AUD": "AUD",
        "CAD": "CAD",
        "BRL": "BRL",
        "TRY": "TRY",
        "JPY": "JPY",
        "SEK": "SEK",
        "NOK": "NOK",
        "DKK": "DKK",
        "CHF": "CHF",
        "NZD": "NZD",
        "MXN": "MXN",
        "AED": "AED",
        "KWD": "KWD",
        "INR": "INR",
        "IDR": "IDR",
        "HKD": "HKD",
        "THB": "THB",
        "SGD": "SGD",
        "PHP": "PHP",
        "MYR": "MYR",
        "SAR": "SAR",
        "ZAR": "ZAR",
        "CNY": "CNY",
        "KRW": "KRW",
        "TWD": "TWD",
    }

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
            "pln|eur|usd|gbp|aud|cad|brl|try|jpy|"
            "sek|nok|dkk|chf|nzd|mxn|aed|kwd|inr|"
            "idr|hkd|thb|sgd|php|myr|sar|zar|cny|"
            "krw|twd"
        )

        patterns = [
            rf"\b(\d+(?:[.,]\d+)?)\s*({currencies})\b",
            rf"\b({currencies})\s*(\d+(?:[.,]\d+)?)\b",
            r"\$(\d+(?:[.,]\d+)?)",
            r"€(\d+(?:[.,]\d+)?)",
            r"£(\d+(?:[.,]\d+)?)",
            r"₹\s*(\d+(?:[.,]\d+)?)",
            r"¥\s*(\d+(?:[.,]\d+)?)",
        ]

        for index, pattern in enumerate(
            patterns
        ):
            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if not match:
                continue

            if index == 0:
                return (
                    ProductExtractor._normalize_number(
                        match.group(1)
                    ),
                    match.group(2).upper()
                )

            if index == 1:
                return (
                    ProductExtractor._normalize_number(
                        match.group(2)
                    ),
                    match.group(1).upper()
                )

            if index == 2:
                return (
                    ProductExtractor._normalize_number(
                        match.group(1)
                    ),
                    "USD"
                )

            if index == 3:
                return (
                    ProductExtractor._normalize_number(
                        match.group(1)
                    ),
                    "EUR"
                )

            if index == 4:
                return (
                    ProductExtractor._normalize_number(
                        match.group(1)
                    ),
                    "GBP"
                )

            if index == 5:
                return (
                    ProductExtractor._normalize_number(
                        match.group(1)
                    ),
                    "INR"
                )

            if index == 6:
                return (
                    ProductExtractor._normalize_number(
                        match.group(1)
                    ),
                    "JPY"
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

        return ProductExtractor._normalize_number(
            match.group(1)
        )

    @staticmethod
    def _normalize_number(value):
        value = str(value).strip()

        if (
            "," in value
            and "." not in value
            and len(value.split(",")[-1]) <= 2
        ):
            return value.replace(
                ",",
                "."
            )

        return (
            value
            .replace(" ", "")
            .replace(",", "")
        )