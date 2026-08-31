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
        original_name = self._canonical_name(
            row.get(
                "clean_name",
                ""
            )
        )

        value, currency = (
            ProductExtractor.extract_money_value(
                original_name
            )
        )

        platform = (
            ProductExtractor.detect_platform(
                row
            )
        )

        name_without_money = self._remove_money(
            original_name,
            value,
            currency
        )

        brand = self._detect_gift_card_brand(
            name_without_money
        )

        if value and currency:
            return self._build_key(
                [
                    "gift-card",
                    brand,
                    value,
                    currency,
                    platform,
                ]
            )

        return self._build_key(
            [
                "gift-card",
                name_without_money,
                platform,
            ]
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

        name_without_money = self._remove_money(
            name,
            value,
            currency
        )

        if value and currency:
            return self._build_key(
                [
                    "crypto-voucher",
                    name_without_money,
                    value,
                    currency,
                ]
            )

        return self._build_key(
            [
                "crypto-voucher",
                name,
            ]
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

        return self._build_key(
            [
                "software",
                name,
                duration,
                (
                    f"{devices}-devices"
                    if devices
                    else ""
                ),
            ]
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

        return self._build_key(
            [
                "subscription",
                name,
                duration,
                platform,
            ]
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

        return self._build_key(
            [
                row[
                    "detected_category"
                ],
                name,
                quantity,
                platform,
            ]
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

        return self._build_key(
            [
                "ingame-item",
                name,
                platform,
            ]
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

        return self._build_key(
            [
                "account",
                name,
                platform,
            ]
        )

    def _service_key(self, row):
        name = self._canonical_name(
            row.get(
                "clean_name",
                ""
            )
        )

        return self._build_key(
            [
                "service",
                name,
            ]
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
    def _detect_gift_card_brand(
        name
    ):
        brands = [
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
            (
                "rewarble",
                [
                    "rewarble",
                ]
            ),
            (
                "binance",
                [
                    "binance",
                ]
            ),
        ]

        for canonical, patterns in brands:
            if any(
                pattern in name
                for pattern in patterns
            ):
                return canonical

        result = re.sub(
            r"\bgift card\b",
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
    def _remove_money(
        name,
        value,
        currency
    ):
        result = name

        if value:
            escaped_value = re.escape(
                value
            )

            result = re.sub(
                rf"\b{escaped_value}\b",
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
            r"[$€£₹¥]",
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