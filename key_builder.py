import re

from extractors import ProductExtractor
from normalizer import TextNormalizer


class SkeletonKeyBuilder:

    def create(self, row):
        category = row["detected_category"]

        if category == "GIFT_CARD":
            return self._gift_card_key(row)

        if category == "SOFTWARE":
            return self._software_key(row)

        if category == "SUBSCRIPTION":
            return self._subscription_key(row)

        if category == "IN_GAME_CURRENCY":
            return self._ingame_currency_key(row)

        if category == "IN_GAME_ITEM":
            return self._ingame_item_key(row)

        if category == "IN_GAME_TOPUP":
            return self._ingame_currency_key(row)

        name = TextNormalizer.clean_product_name(
            row.get("clean_name", "")
        )

        return TextNormalizer.slugify(
            f"{category}-{name}"
        )

    def _gift_card_key(self, row):
        name = TextNormalizer.clean_product_name(
            row.get("clean_name", "")
        )

        value, currency = ProductExtractor.extract_money_value(
            name
        )

        platform = ProductExtractor.detect_platform(row)
        region = ProductExtractor.detect_region(row)

        if value:
            name = re.sub(
                rf"\b{re.escape(value)}\b",
                " ",
                name
            )

        if currency:
            name = re.sub(
                rf"\b{currency.lower()}\b",
                " ",
                name
            )

        name = re.sub(
            r"\s+",
            " ",
            name
        ).strip()

        elements = [
            "gift-card",
            name,
            value,
            currency,
            platform,
            region,
        ]

        return self._build_key(elements)

    def _software_key(self, row):
        name = TextNormalizer.clean_product_name(
            row.get("clean_name", "")
        )

        duration = ProductExtractor.extract_duration(name)
        devices = ProductExtractor.extract_devices(name)
        region = ProductExtractor.detect_region(row)

        elements = [
            "software",
            name,
            duration,
            f"{devices}-devices" if devices else "",
            region,
        ]

        return self._build_key(elements)

    def _subscription_key(self, row):
        name = TextNormalizer.clean_product_name(
            row.get("clean_name", "")
        )

        duration = ProductExtractor.extract_duration(name)
        platform = ProductExtractor.detect_platform(row)
        region = ProductExtractor.detect_region(row)

        elements = [
            "subscription",
            name,
            duration,
            platform,
            region,
        ]

        return self._build_key(elements)

    def _ingame_currency_key(self, row):
        name = TextNormalizer.clean_product_name(
            row.get("clean_name", "")
        )

        platform = ProductExtractor.detect_platform(row)
        region = ProductExtractor.detect_region(row)

        elements = [
            "ingame-currency",
            name,
            platform,
            region,
        ]

        return self._build_key(elements)

    def _ingame_item_key(self, row):
        name = TextNormalizer.clean_product_name(
            row.get("clean_name", "")
        )

        platform = ProductExtractor.detect_platform(row)
        region = ProductExtractor.detect_region(row)

        elements = [
            "ingame-item",
            name,
            platform,
            region,
        ]

        return self._build_key(elements)

    @staticmethod
    def _build_key(elements):
        value = "-".join(
            element
            for element in elements
            if element
        )

        return TextNormalizer.slugify(value)