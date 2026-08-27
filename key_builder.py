import re

from extractors import ProductExtractor
from normalizer import TextNormalizer


class SkeletonKeyBuilder:

    def create(self, row):
        category = row[
            "detected_category"
        ]

        if category == "GIFT_CARD":
            return self._gift_card_key(
                row
            )

        if category == "CRYPTO_VOUCHER":
            return self._crypto_voucher_key(
                row
            )

        if category == "SOFTWARE":
            return self._software_key(
                row
            )

        if category == "SUBSCRIPTION":
            return self._subscription_key(
                row
            )

        if category in {
            "IN_GAME_CURRENCY",
            "IN_GAME_TOPUP",
            "TOP_UP",
        }:
            return self._currency_or_topup_key(
                row
            )

        if category == "IN_GAME_ITEM":
            return self._ingame_item_key(
                row
            )

        if category == "ACCOUNT":
            return self._account_key(
                row
            )

        if category == "IN_GAME_SERVICE":
            return self._service_key(
                row
            )

        name = self._canonical_name(
            row.get(
                "clean_name",
                ""
            )
        )

        return self._build_key(
            [
                category,
                name,
            ]
        )

    def _gift_card_key(self, row):
        name = self._canonical_name(
            row.get(
                "clean_name",
                ""
            )
        )

        value, currency = (
            ProductExtractor.extract_money_value(
                name
            )
        )

        platform = (
            ProductExtractor.detect_platform(
                row
            )
        )

        name = self._remove_money(
            name,
            value,
            currency
        )

        name = self._canonical_gift_card_brand(
            name
        )

        elements = [
            "gift-card",
            name,
            value,
            currency,
            platform,
        ]

        return self._build_key(
            elements
        )

    def _crypto_voucher_key(self, row):
        name = self._canonical_name(
            row.get(
                "clean_name",
                ""
            )
        )

        value, currency = (
            ProductExtractor.extract_money_value(
                name
            )
        )

        name = self._remove_money(
            name,
            value,
            currency
        )

        elements = [
            "crypto-voucher",
            name,
            value,
            currency,
        ]

        return self._build_key(
            elements
        )

    def _software_key(self, row):
        name = self._canonical_name(
            row.get(
                "clean_name",
                ""
            )
        )

        duration = (
            ProductExtractor.extract_duration(
                name
            )
        )

        devices = (
            ProductExtractor.extract_devices(
                name
            )
        )

        name = self._remove_duration(
            name
        )

        name = self._remove_devices(
            name
        )

        elements = [
            "software",
            name,
            duration,
            (
                f"{devices}-devices"
                if devices
                else ""
            ),
        ]

        return self._build_key(
            elements
        )

    def _subscription_key(self, row):
        name = self._canonical_name(
            row.get(
                "clean_name",
                ""
            )
        )

        duration = (
            ProductExtractor.extract_duration(
                name
            )
        )

        platform = (
            ProductExtractor.detect_platform(
                row
            )
        )

        name = self._remove_duration(
            name
        )

        elements = [
            "subscription",
            name,
            duration,
            platform,
        ]

        return self._build_key(
            elements
        )

    def _currency_or_topup_key(
        self,
        row
    ):
        name = self._canonical_name(
            row.get(
                "clean_name",
                ""
            )
        )

        platform = (
            ProductExtractor.detect_platform(
                row
            )
        )

        quantity = (
            ProductExtractor.extract_quantity(
                name,
                [
                    "v-bucks",
                    "v bucks",
                    "vbucks",
                    "robux",
                    "points",
                    "coins",
                    "credits",
                    "rp",
                    "gold",
                ]
            )
        )

        elements = [
            row["detected_category"],
            name,
            quantity,
            platform,
        ]

        return self._build_key(
            elements
        )

    def _ingame_item_key(self, row):
        name = self._canonical_name(
            row.get(
                "clean_name",
                ""
            )
        )

        platform = (
            ProductExtractor.detect_platform(
                row
            )
        )

        elements = [
            "ingame-item",
            name,
            platform,
        ]

        return self._build_key(
            elements
        )

    def _account_key(self, row):
        name = self._canonical_name(
            row.get(
                "clean_name",
                ""
            )
        )

        platform = (
            ProductExtractor.detect_platform(
                row
            )
        )

        elements = [
            "account",
            name,
            platform,
        ]

        return self._build_key(
            elements
        )

    def _service_key(self, row):
        name = self._canonical_name(
            row.get(
                "clean_name",
                ""
            )
        )

        elements = [
            "service",
            name,
        ]

        return self._build_key(
            elements
        )

    @staticmethod
    def _canonical_name(text):
        text = (
            TextNormalizer.clean_product_name(
                text
            )
        )

        replacements = {
            r"\bplaystation network\b":
                "playstation",

            r"\bpsn\b":
                "playstation",

            r"\bplaystation store\b":
                "playstation",

            r"\bsteam wallet\b":
                "steam",

            r"\bnintendo e[- ]?shop\b":
                "nintendo",

            r"\bmicrosoft xbox\b":
                "xbox",

            r"\bxbox live\b":
                "xbox",

            r"\bgiftcard\b":
                "gift card",

            r"\bgift-card\b":
                "gift card",

            r"\bwallet card\b":
                "gift card",

            r"\bwallet code\b":
                "gift card",

            r"\bprepaid card\b":
                "gift card",

            r"\bpre-paid card\b":
                "gift card",
        }

        for pattern, replacement in (
            replacements.items()
        ):
            text = re.sub(
                pattern,
                replacement,
                text
            )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    @staticmethod
    def _canonical_gift_card_brand(
        name
    ):
        brand_patterns = [
            (
                "playstation",
                [
                    "playstation",
                ]
            ),

            (
                "xbox",
                [
                    "xbox",
                ]
            ),

            (
                "steam",
                [
                    "steam",
                ]
            ),

            (
                "nintendo",
                [
                    "nintendo",
                ]
            ),

            (
                "google-play",
                [
                    "google play",
                ]
            ),

            (
                "apple",
                [
                    "apple",
                    "itunes",
                ]
            ),

            (
                "amazon",
                [
                    "amazon",
                ]
            ),

            (
                "instant-gaming",
                [
                    "instant gaming",
                ]
            ),

            (
                "roblox",
                [
                    "roblox",
                ]
            ),
        ]

        for canonical, words in (
            brand_patterns
        ):
            if any(
                word in name
                for word in words
            ):
                return canonical

        name = re.sub(
            r"\bgift card\b",
            " ",
            name
        )

        name = re.sub(
            r"\s+",
            " ",
            name
        )

        return name.strip()

    @staticmethod
    def _remove_money(
        name,
        value,
        currency
    ):
        result = name

        if value:
            result = re.sub(
                rf"\b{re.escape(value)}\b",
                " ",
                result
            )

        if currency:
            result = re.sub(
                rf"\b{re.escape(currency.lower())}\b",
                " ",
                result
            )

        result = re.sub(
            r"[$€£]",
            " ",
            result
        )

        result = re.sub(
            r"\s+",
            " ",
            result
        )

        return result.strip()

    @staticmethod
    def _remove_duration(name):
        result = re.sub(
            r"\b\d+\s*"
            r"(day|days|month|months|year|years)\b",
            " ",
            name
        )

        result = re.sub(
            r"\s+",
            " ",
            result
        )

        return result.strip()

    @staticmethod
    def _remove_devices(name):
        result = re.sub(
            r"\b\d+\s*devices?\b",
            " ",
            name
        )

        result = re.sub(
            r"\s+",
            " ",
            result
        )

        return result.strip()

    @staticmethod
    def _build_key(elements):
        value = "-".join(
            str(element)
            for element in elements
            if element
        )

        return TextNormalizer.slugify(
            value
        )