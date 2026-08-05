from normalizer import TextNormalizer


class ProductClassifier:

    FEED_MAPPING = {
        "software": "SOFTWARE",
        "ingame_currency": "IN_GAME_CURRENCY",
        "ingame_item": "IN_GAME_ITEM",
        "ingame_topup": "IN_GAME_TOPUP",
        "ingame_account": "ACCOUNT",
        "ingame_boosting": "IN_GAME_SERVICE",
        "csgo_skins": "IN_GAME_ITEM",
        "mobile_topup": "TOP_UP",
        "prepaid": "GIFT_CARD",
        "gift cards": "GIFT_CARD",
        "crypto_vouchers": "GIFT_CARD",
    }

    INGAME_CURRENCY_WORDS = [
        "v-bucks",
        "v bucks",
        "robux",
        "fc points",
        "fifa points",
        "riot points",
        "valorant points",
        "cod points",
        "call of duty points",
        "minecoins",
        "wow gold",
        "osrs gold",
        "runescape gold",
    ]

    GIFT_CARD_WORDS = [
        "gift card",
        "giftcard",
        "wallet card",
        "wallet code",
        "prepaid card",
        "store card",
        "voucher",
    ]

    SUBSCRIPTION_WORDS = [
        "game pass",
        "playstation plus",
        "ps plus",
        "nintendo switch online",
        "ea play",
        "ubisoft+",
        "ubisoft plus",
        "membership",
        "subscription",
    ]

    SOFTWARE_WORDS = [
        "windows 10",
        "windows 11",
        "microsoft office",
        "office 365",
        "microsoft 365",
        "antivirus",
        "internet security",
        "vpn",
        "webroot",
        "kaspersky",
        "norton",
        "bitdefender",
        "avast",
        "adobe",
    ]

    INGAME_ITEM_WORDS = [
        "skin",
        "skins",
        "weapon skin",
        "player trade",
        "mount",
        "in-game item",
    ]

    def classify(self, row):
        name = TextNormalizer.normalize(
            f"{row.get('clean_name', '')} "
            f"{row.get('original_name', '')}"
        )

        feed_category = TextNormalizer.normalize(
            row.get("feed_category", "")
        )

        category = TextNormalizer.normalize(
            row.get("category", "")
        )

        if feed_category in self.FEED_MAPPING:
            product_type = self.FEED_MAPPING[feed_category]

            return (
                product_type,
                0.98,
                f"feed_category:{feed_category}"
            )

        if category in {
            "game_gift",
            "gift_card",
            "gift card"
        }:
            return (
                "GIFT_CARD",
                0.96,
                f"category:{category}"
            )

        result = self._find_keyword(
            name,
            self.INGAME_CURRENCY_WORDS,
            "IN_GAME_CURRENCY",
            0.95
        )

        if result:
            return result

        result = self._find_keyword(
            name,
            self.GIFT_CARD_WORDS,
            "GIFT_CARD",
            0.94
        )

        if result:
            return result

        result = self._find_keyword(
            name,
            self.SUBSCRIPTION_WORDS,
            "SUBSCRIPTION",
            0.94
        )

        if result:
            return result

        result = self._find_keyword(
            name,
            self.SOFTWARE_WORDS,
            "SOFTWARE",
            0.92
        )

        if result:
            return result

        result = self._find_keyword(
            name,
            self.INGAME_ITEM_WORDS,
            "IN_GAME_ITEM",
            0.90
        )

        if result:
            return result

        return (
            "OTHER",
            0.20,
            "no_rule"
        )

    @staticmethod
    def _find_keyword(
        text,
        words,
        product_type,
        confidence
    ):
        for word in words:
            if word in text:
                return (
                    product_type,
                    confidence,
                    f"keyword:{word}"
                )

        return None