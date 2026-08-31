from normalizer import TextNormalizer


class ProductClassifier:

    FEED_MAPPING = {
        "software": "SOFTWARE",
        "ingame_currency": "IN_GAME_CURRENCY",
        "ingame_item": "IN_GAME_ITEM",
        "ingame_topup": "IN_GAME_TOPUP",
        "ingame_account": "ACCOUNT",
        "game_account": "ACCOUNT",
        "ingame_boosting": "IN_GAME_SERVICE",
        "csgo_skins": "IN_GAME_ITEM",
        "mobile_topup": "TOP_UP",
        "mobile_topup_gc": "TOP_UP",
        "direct top-up": "TOP_UP",
        "prepaid": "GIFT_CARD",
        "gift cards": "GIFT_CARD",
        "gift_card": "GIFT_CARD",
        "crypto_vouchers": "CRYPTO_VOUCHER",
        "subscriptions": "SUBSCRIPTION",
        "subscription": "SUBSCRIPTION",
        "steam top up": "TOP_UP",
        "game points": "IN_GAME_CURRENCY",
        "league of legends rp": "IN_GAME_CURRENCY",
        "hosting": "SOFTWARE",
    }

    CATEGORY_MAPPING = {
        "gift card": "GIFT_CARD",
        "gift_card": "GIFT_CARD",
        "software": "SOFTWARE",
        "subscription": "SUBSCRIPTION",
        "account": "ACCOUNT",
        "game_account": "ACCOUNT",
        "ingame item": "IN_GAME_ITEM",
        "ingame_item": "IN_GAME_ITEM",
        "ingame currency": "IN_GAME_CURRENCY",
        "ingame_currency": "IN_GAME_CURRENCY",
    }

    EXISTING_PIPELINE_CATEGORIES = {
        "game",
        "games",
        "game_gift",
        "game gift",
        "dlc",
        "dlc_gift",
        "dlc gift",
        "dlc_account",
        "dlc account",
        "game_preorder",
        "game preorder",
        "game_preorder_gift",
        "game preorder gift",
        "game_preorder_account",
        "game preorder account",
        "dlc_preorder",
        "dlc preorder",
        "dlc_preorder_gift",
        "dlc preorder gift",
        "dlc_preorder_account",
        "dlc preorder account",
        "preorder",
    }

    DRM_MAPPING = {
        "crypto voucher": "CRYPTO_VOUCHER",
        "cryptovoucher": "CRYPTO_VOUCHER",
        "gift me crypto": "CRYPTO_VOUCHER",
        "giftmecrypto": "CRYPTO_VOUCHER",
        "roblox": "IN_GAME_CURRENCY",
        "riot": "IN_GAME_CURRENCY",
        "in app": "IN_GAME_ITEM",
    }

    CRYPTO_WORDS = [
        "crypto voucher",
        "crypto gift card",
        "gift me crypto",
        "giftmecrypto",
        "rewarble crypto",
        "cryptovoucher",
    ]

    INGAME_CURRENCY_WORDS = [
        "v-bucks",
        "v bucks",
        "vbucks",
        "robux",
        "fc points",
        "fifa points",
        "riot points",
        "valorant points",
        "cod points",
        "call of duty points",
        "minecoins",
        "wow gold",
        "world of warcraft gold",
        "osrs gold",
        "runescape gold",
        "guild wars gold",
        "apex coins",
        "overwatch coins",
        "genshin crystals",
        "genesis crystals",
        "shark card",
    ]

    GIFT_CARD_WORDS = [
        "gift card",
        "giftcard",
        "gift-card",
        "wallet card",
        "wallet code",
        "wallet voucher",
        "prepaid card",
        "pre-paid card",
        "store card",
        "gift voucher",
        "digital voucher",
        "psn card",
        "playstation store card",
        "xbox gift card",
        "steam gift card",
        "steam wallet",
        "nintendo eshop card",
        "google play card",
        "apple gift card",
        "itunes gift card",
        "amazon gift card",
    ]

    SUBSCRIPTION_WORDS = [
        "game pass",
        "gamepass",
        "xbox live gold",
        "playstation plus",
        "ps plus",
        "ps+",
        "nintendo switch online",
        "ea play",
        "ubisoft+",
        "ubisoft plus",
        "wow subscription",
        "subscription",
        "premium subscription",
    ]

    SOFTWARE_WORDS = [
        "windows 10",
        "windows 11",
        "windows server",
        "microsoft office",
        "office 2016",
        "office 2019",
        "office 2021",
        "office 2024",
        "office 365",
        "microsoft 365",
        "antivirus",
        "internet security",
        "total security",
        "vpn",
        "webroot",
        "kaspersky",
        "norton",
        "bitdefender",
        "avast",
        "avg",
        "mcafee",
        "adobe",
        "photoshop",
        "illustrator",
        "acrobat",
        "autocad",
        "autodesk",
        "vmware",
        "winrar",
        "malwarebytes",
    ]

    INGAME_ITEM_WORDS = [
        "weapon skin",
        "character skin",
        "player skin",
        "skin",
        "skins",
        "mount",
        "pet",
        "loot box",
        "cs2 skin",
        "csgo skin",
        "knife skin",
        "player trade",
        "in-game item",
        "in game item",
    ]

    ACCOUNT_WORDS = [
        "game account",
        "gaming account",
        "starter account",
        "fresh account",
        "full access account",
        "smurf account",
        "leveled account",
    ]

    SERVICE_WORDS = [
        "boosting",
        "rank boosting",
        "rank boost",
        "power leveling",
        "powerleveling",
        "leveling service",
        "coaching service",
        "carry service",
    ]

    TOPUP_WORDS = [
        "mobile top up",
        "mobile top-up",
        "phone top up",
        "phone top-up",
        "mobile recharge",
        "direct top up",
        "direct top-up",
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

        drm = TextNormalizer.normalize(
            row.get("drm", "")
        )

        result = self._classify_crypto(
            name,
            drm,
            feed_category
        )

        if result:
            return result

        result = self._classify_from_feed(
            feed_category
        )

        if result:
            return result

        result = self._classify_from_category(
            category
        )

        if result:
            return result

        result = self._classify_from_drm(
            drm
        )

        if result:
            return result

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
            0.93
        )

        if result:
            return result

        result = self._classify_membership(
            name
        )

        if result:
            return result

        result = self._find_keyword(
            name,
            self.ACCOUNT_WORDS,
            "ACCOUNT",
            0.92
        )

        if result:
            return result

        result = self._find_keyword(
            name,
            self.SERVICE_WORDS,
            "IN_GAME_SERVICE",
            0.92
        )

        if result:
            return result

        result = self._find_keyword(
            name,
            self.TOPUP_WORDS,
            "TOP_UP",
            0.91
        )

        if result:
            return result

        result = self._find_keyword(
            name,
            self.SOFTWARE_WORDS,
            "SOFTWARE",
            0.90
        )

        if result:
            return result

        result = self._find_keyword(
            name,
            self.INGAME_ITEM_WORDS,
            "IN_GAME_ITEM",
            0.88
        )

        if result:
            return result

        result = self._classify_existing_pipeline(
            category
        )

        if result:
            return result

        return (
            "OTHER",
            0.20,
            "no_rule"
        )

    def _classify_crypto(
        self,
        name,
        drm,
        feed_category
    ):
        if feed_category == "crypto_vouchers":
            return (
                "CRYPTO_VOUCHER",
                0.99,
                "feed_category:crypto_vouchers"
            )

        for word in self.CRYPTO_WORDS:
            if word in name or word in drm:
                return (
                    "CRYPTO_VOUCHER",
                    0.97,
                    f"crypto:{word}"
                )

        return None

    def _classify_from_feed(
        self,
        feed_category
    ):
        if not feed_category:
            return None

        if feed_category in self.FEED_MAPPING:
            return (
                self.FEED_MAPPING[feed_category],
                0.99,
                f"feed_category:{feed_category}"
            )

        return None

    def _classify_from_category(
        self,
        category
    ):
        if not category:
            return None

        if category in self.CATEGORY_MAPPING:
            return (
                self.CATEGORY_MAPPING[category],
                0.96,
                f"category:{category}"
            )

        return None

    def _classify_from_drm(
        self,
        drm
    ):
        if not drm:
            return None

        if drm in self.DRM_MAPPING:
            return (
                self.DRM_MAPPING[drm],
                0.90,
                f"drm:{drm}"
            )

        return None

    def _classify_existing_pipeline(
        self,
        category
    ):
        if not category:
            return None

        if category in self.EXISTING_PIPELINE_CATEGORIES:
            return (
                "EXISTING_PIPELINE",
                1.0,
                f"existing_pipeline:{category}"
            )

        return None

    def _classify_membership(
        self,
        name
    ):
        if "membership" not in name:
            return None

        duration_words = [
            "month",
            "months",
            "year",
            "years",
            "day",
            "days",
        ]

        known_services = [
            "nintendo switch online",
            "playstation plus",
            "xbox live",
            "ea play",
            "ubisoft plus",
            "ubisoft+",
        ]

        if any(
            word in name
            for word in duration_words
        ):
            return (
                "SUBSCRIPTION",
                0.88,
                "keyword:membership_with_duration"
            )

        if any(
            service in name
            for service in known_services
        ):
            return (
                "SUBSCRIPTION",
                0.90,
                "keyword:membership_service"
            )

        return None

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