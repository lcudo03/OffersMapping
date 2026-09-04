import re

from normalizer import TextNormalizer


class BrandDetector:

    BRAND_PATTERNS = [
        ("League of Legends", [
            "league of legends",
            "lol rp",
        ]),
        ("Valorant", [
            "valorant",
        ]),
        ("Fortnite", [
            "fortnite",
            "v-bucks",
            "v bucks",
            "vbucks",
        ]),
        ("Roblox", [
            "roblox",
            "robux",
        ]),
        ("Garena Free Fire", [
            "garena free fire",
            "free fire",
        ]),
        ("PUBG Mobile", [
            "pubg mobile",
            "playerunknown's battlegrounds mobile",
            "playerunknowns battlegrounds mobile",
        ]),
        ("Warframe", [
            "warframe",
        ]),
        ("Dofus", [
            "dofus",
        ]),
        ("OSRS", [
            "osrs",
            "old school runescape",
            "oldschool runescape",
        ]),
        ("RuneScape", [
            "runescape",
        ]),
        ("Tamashi: Rise of Yokai", [
            "tamashi: rise of yokai",
            "tamashi rise of yokai",
        ]),
        ("Dynasty Warriors: Overlords", [
            "dynasty warriors: overlords",
            "dynasty warriors overlords",
        ]),
        ("Bleach: Soul Resonance", [
            "bleach: soul resonance",
            "bleach soul resonance",
        ]),
        ("Arena Breakout", [
            "arena breakout",
        ]),
        ("Raid: Shadow Legends", [
            "raid: shadow legends",
            "raid shadow legends",
        ]),
        ("Watcher of Realms", [
            "watcher of realms",
        ]),
        ("Brawl Stars", [
            "brawl stars",
        ]),
        ("Honkai: Star Rail", [
            "honkai: star rail",
            "honkai star rail",
        ]),
        ("Arknights: Endfield", [
            "arknights: endfield",
            "arknights endfield",
        ]),
        ("Adopt Me", [
            "adopt me",
        ]),
        ("ARC Raiders", [
            "arc raiders",
        ]),
        ("Type Soul", [
            "type soul",
        ]),
        ("Mobile Legends", [
            "mobile legends",
            "mobile legends bang bang",
            "mobile legends: bang bang",
            "mlbb",
        ]),
        ("Diablo IV", [
            "diablo iv",
            "diablo 4",
        ]),
        ("The Elder Scrolls Online", [
            "the elder scrolls online",
            "elder scrolls online",
            "eso gold",
            "eso crowns",
            "eso",
        ]),
        ("EA Sports FC", [
            "ea sports fc",
            "fc 24",
            "fc24",
            "fc 25",
            "fc25",
            "fc 26",
            "fc26",
            "fut coins",
        ]),
        ("The Sims", [
            "the sims",
            "sims 4",
        ]),
        ("Delta Force", [
            "delta force",
        ]),
        ("Gran Turismo", [
            "gran turismo",
        ]),
        ("Blood Strike", [
            "blood strike",
        ]),
        ("Whiteout Survival", [
            "whiteout survival",
        ]),
        ("Racing Master", [
            "racing master",
        ]),
        ("Eggy Party", [
            "eggy party",
        ]),
        ("Black Myth: Wukong", [
            "black myth: wukong",
            "black myth wukong",
        ]),
        ("Final Fantasy XIV", [
            "final fantasy xiv",
            "final fantasy 14",
            "ffxiv",
            "ff14",
        ]),
        ("Ashes of Creation", [
            "ashes of creation",
        ]),
        ("ONE PUNCH MAN: The Strongest", [
            "one punch man: the strongest",
            "one punch man the strongest",
        ]),
        ("Dungeonborne", [
            "dungeonborne",
        ]),
        ("Cyberpunk 2077", [
            "cyberpunk 2077",
        ]),
        ("SMITE", [
            "smite",
            "smite 2",
        ]),
        ("Forza Horizon", [
            "forza horizon",
        ]),
        ("Dragon Raja", [
            "dragon raja",
        ]),
        ("Identity V", [
            "identity v",
            "identity 5",
        ]),
        ("Undecember", [
            "undecember",
        ]),
        ("Sword of Justice", [
            "sword of justice",
        ]),

        ("PlayStation", [
            "playstation network",
            "playstation store",
            "playstation",
            "psn",
            "ps plus",
        ]),
        ("Xbox", [
            "xbox game pass",
            "xbox live",
            "xbox",
            "game pass",
        ]),
        ("Nintendo", [
            "nintendo eshop",
            "nintendo e-shop",
            "nintendo switch",
            "nintendo",
        ]),
        ("Steam", [
            "steam wallet",
            "steam",
        ]),
        ("Epic Games", [
            "epic games",
            "epic games store",
        ]),
        ("Battle.net", [
            "battle.net",
            "battle net",
        ]),
        ("Meta Quest", [
            "meta quest",
            "oculus quest",
            "oculus",
        ]),

        ("Amazon", [
            "amazon",
        ]),
        ("Google Play", [
            "google play",
        ]),
        ("Apple", [
            "apple gift card",
            "itunes",
            "app store",
        ]),
        ("PayPal", [
            "paypal",
        ]),
        ("Razer Gold", [
            "razer gold",
        ]),
        ("Mifinity", [
            "mifinity",
            "mi finity",
        ]),
        ("Birkenstock", [
            "birkenstock",
        ]),

        ("Microsoft Office", [
            "microsoft office",
            "office 2016",
            "office 2019",
            "office 2021",
            "office 2024",
        ]),
        ("Microsoft 365", [
            "microsoft 365",
            "office 365",
        ]),
        ("Windows", [
            "windows 10",
            "windows 11",
            "windows server",
        ]),
        ("Adobe", [
            "adobe",
            "photoshop",
            "illustrator",
            "acrobat",
        ]),
        ("Autodesk", [
            "autodesk",
            "autocad",
        ]),
        ("VMware", [
            "vmware",
        ]),
        ("Norton", [
            "norton",
        ]),
        ("Kaspersky", [
            "kaspersky",
        ]),
        ("Bitdefender", [
            "bitdefender",
        ]),
        ("Avast", [
            "avast",
        ]),
        ("AVG", [
            "avg",
        ]),
        ("McAfee", [
            "mcafee",
        ]),
        ("Malwarebytes", [
            "malwarebytes",
        ]),
        ("Webroot", [
            "webroot",
        ]),
        ("F-Secure", [
            "f-secure",
            "f secure",
        ]),
        ("WinRAR", [
            "winrar",
        ]),
        ("Ashampoo", [
            "ashampoo",
        ]),
        ("MAGIX", [
            "magix",
        ]),
        ("Corel", [
            "corel",
            "coreldraw",
            "corel draw",
        ]),
        ("IObit", [
            "iobit",
        ]),
        ("MiniTool", [
            "minitool",
            "mini tool",
        ]),
        ("CyberLink", [
            "cyberlink",
            "powerdirector",
            "photodirector",
        ]),
        ("Trend Micro", [
            "trend micro",
        ]),
        ("Pinnacle Studio", [
            "pinnacle studio",
        ]),
        ("VEGAS Pro", [
            "vegas pro",
            "sony vegas",
        ]),
        ("G Data", [
            "g data",
            "g-data",
        ]),
        ("IK Multimedia", [
            "ik multimedia",
        ]),

        ("Rewarble", [
            "rewarble",
        ]),
        ("Gift Me Crypto", [
            "gift me crypto",
            "giftmecrypto",
        ]),
        ("Crypto Voucher", [
            "crypto voucher",
            "cryptovoucher",
        ]),
        ("Cryptonow", [
            "cryptonow",
            "crypto now",
        ]),
        ("BitJem", [
            "bitjem",
            "bit jem",
        ]),
        ("Binance", [
            "binance",
        ]),

        ("Counter-Strike", [
            "counter-strike",
            "counter strike",
            "csgo",
            "cs2",
        ]),
        ("Call of Duty", [
            "call of duty",
            "cod points",
        ]),
        ("World of Warcraft", [
            "world of warcraft",
            "wow gold",
            "wow subscription",
        ]),
        ("Minecraft", [
            "minecraft",
            "minecoins",
        ]),
        ("Apex Legends", [
            "apex legends",
            "apex coins",
        ]),
        ("Overwatch", [
            "overwatch",
        ]),
        ("Genshin Impact", [
            "genshin impact",
            "genesis crystals",
        ]),

        ("Netflix", [
            "netflix",
        ]),
        ("Spotify", [
            "spotify",
        ]),
        ("TikTok", [
            "tiktok",
            "tik tok",
        ]),
        ("Sweet.tv", [
            "sweet.tv",
            "sweet tv",
        ]),
        ("Uber", [
            "uber eats",
            "uber",
        ]),
        ("Just Eat", [
            "just eat",
        ]),
        ("Ticketmaster", [
            "ticketmaster",
        ]),
        ("Starbucks", [
            "starbucks",
        ]),
        ("Sephora", [
            "sephora",
        ]),
        ("Decathlon", [
            "decathlon",
        ]),
        ("Foot Locker", [
            "foot locker",
            "footlocker",
        ]),
        ("OnlyFans", [
            "onlyfans",
        ]),
        ("Fansly", [
            "fansly",
        ]),
        ("H&M", [
            "h&m",
            "h and m",
        ]),
        ("Bath & Body Works", [
            "bath & body works",
            "bath and body works",
            "bath body works",
        ]),
        ("LEGO", [
            "lego",
        ]),
        ("The Home Depot", [
            "the home depot",
            "home depot",
        ]),
        ("TK Maxx", [
            "tk maxx",
        ]),
        ("Maisons du Monde", [
            "maisons du monde",
        ]),
        ("Lotte Mart", [
            "lotte mart",
        ]),
        ("Poppo Live", [
            "poppo live",
        ]),
        ("1-800-Flowers", [
            "1-800-flowers",
            "1 800 flowers",
            "1800flowers",
        ]),
    ]

    CATEGORY_MARKERS = {
        "GIFT_CARD": [
            "e-gift card",
            "egift card",
            "gift card",
            "giftcard",
            "gift-card",
            "prepaid card",
            "pre-paid card",
            "voucher",
        ],

        "CRYPTO_VOUCHER": [
            "crypto gift card",
            "crypto voucher",
            "gift card",
            "voucher",
        ],

        "SUBSCRIPTION": [
            "subscription",
            "membership",
            "premium subscription",
        ],

        "TOP_UP": [
            "direct top-up",
            "direct top up",
            "mobile top-up",
            "mobile top up",
            "top-up",
            "top up",
        ],

        "IN_GAME_TOPUP": [
            "direct top-up",
            "direct top up",
            "top-up",
            "top up",
        ],

        "ACCOUNT": [
            "accounts",
            "account",
        ],

        "IN_GAME_ITEM": [
            "items",
            "item",
        ],

        "IN_GAME_CURRENCY": [
            "currency",
        ],

        "IN_GAME_SERVICE": [
            "boosting",
            "boost",
            "services",
            "service",
        ],
    }

    GENERAL_MARKERS = [
        "e-gift card",
        "egift card",
        "gift card",
        "giftcard",
        "gift-card",
        "prepaid card",
        "pre-paid card",
        "voucher",

        "accounts",
        "account",

        "items",
        "item",

        "boosting",
        "boost",

        "currency",

        "direct top-up",
        "direct top up",
        "mobile top-up",
        "mobile top up",
        "top-up",
        "top up",

        "subscriptions",
        "subscription",

        "memberships",
        "membership",

        "services",
        "service",
    ]

    VARIANT_WORDS = {
        "direct",
        "package",
        "bundle",
        "pack",
        "code",
        "key",
        "digital",
        "online",
        "instant",
        "activation",
        "premium",
        "monthly",
        "annual",
        "yearly",
        "standard",
        "deluxe",
        "ultimate",
        "edition",
        "pass",
        "card",
        "voucher",
    }

    STORE_SUFFIXES = [
        r"\bmicrosoft store\b",
        r"\bplaystation store\b",
        r"\bnintendo e-?shop\b",
        r"\bepic games store\b",
        r"\bgoogle play\b",
        r"\bapp store\b",
    ]

    PLATFORM_PATTERNS = [
        r"\bpc\b",
        r"\bandroid\b",
        r"\bios\b",

        r"\bps4\b",
        r"\bps5\b",
        r"\bplaystation 4\b",
        r"\bplaystation 5\b",

        r"\bxbox one\b",
        r"\bxbox series x\b",
        r"\bxbox series s\b",
        r"\bxbox series x/s\b",

        r"\bnintendo switch\b",
    ]

    REGION_PATTERNS = [
        r"\bglobal\b",
        r"\bworldwide\b",
        r"\bregion free\b",

        r"\bnorth america\b",
        r"\bsouth america\b",

        r"\bunited states\b",
        r"\bunited kingdom\b",

        r"\beuropean union\b",
        r"\beurope\b",

        r"\bgreat britain\b",

        r"\bpoland\b",
        r"\bgermany\b",
        r"\bfrance\b",
        r"\bitaly\b",
        r"\bspain\b",
        r"\bturkey\b",
        r"\baustralia\b",
        r"\bcanada\b",
        r"\bbrazil\b",
        r"\bjapan\b",

        r"\busa\b",
        r"\bus\b",
        r"\beu\b",
        r"\buk\b",
        r"\bau\b",
    ]

    CURRENCIES = (
        "pln|eur|usd|gbp|aud|cad|brl|try|jpy|"
        "sek|nok|dkk|chf|nzd|mxn|aed|kwd|inr|"
        "idr|hkd|thb|sgd|php|myr|sar|zar|cny|"
        "krw|twd"
    )

    @classmethod
    def detect(cls, row):
        clean_name = cls._normalize(
            row.get("clean_name", "")
        )

        original_name = cls._normalize(
            row.get("original_name", "")
        )

        category = str(
            row.get(
                "detected_category",
                row.get("category", "")
            )
        ).upper()

        combined = (
            clean_name
            + " "
            + original_name
        ).strip()

        if not combined:
            return "Unknown"

        known = cls._detect_known_brand(
            combined
        )

        if known:
            return known

        sources = []

        if clean_name:
            sources.append(clean_name)

        if (
            original_name
            and original_name != clean_name
        ):
            sources.append(original_name)

        for text in sources:

            hierarchical = (
                cls._extract_hierarchical_brand(
                    text
                )
            )

            if hierarchical:
                return hierarchical

            category_brand = (
                cls._extract_by_category(
                    text,
                    category
                )
            )

            if category_brand:
                return category_brand

            marker_brand = (
                cls._extract_before_markers(
                    text,
                    cls.GENERAL_MARKERS
                )
            )

            if marker_brand:
                return marker_brand

            dash_brand = (
                cls._extract_before_dash(
                    text
                )
            )

            if dash_brand:
                return dash_brand

            fallback = cls._fallback_brand(
                text
            )

            if fallback:
                return fallback

        return "Unknown"

    @classmethod
    def canonical_key(cls, name):
        if not name:
            return "unknown"

        value = cls._normalize(
            name
        )

        if not value:
            return "unknown"

        value = value.replace(
            "&",
            " and "
        )

        value = re.sub(
            r"\band\b",
            " ",
            value
        )

        value = re.sub(
            r"^\s*the\s+",
            "",
            value
        )

        value = re.sub(
            r"\b1[\s-]*800[\s-]*flowers\b",
            "1800flowers",
            value
        )

        value = re.sub(
            r"[^a-z0-9]+",
            " ",
            value
        )

        value = re.sub(
            r"\s+",
            " ",
            value
        ).strip()

        if not value:
            return "unknown"

        return TextNormalizer.slugify(
            value
        )

    @staticmethod
    def _normalize(value):
        if value is None:
            return ""

        value = str(value).strip()

        if not value:
            return ""

        if value.lower() == "nan":
            return ""

        return TextNormalizer.normalize(
            value
        )

    @classmethod
    def _detect_known_brand(
        cls,
        text
    ):
        aliases = []

        for brand, patterns in cls.BRAND_PATTERNS:
            for pattern in patterns:
                aliases.append(
                    (
                        brand,
                        cls._normalize(pattern)
                    )
                )

        aliases.sort(
            key=lambda value: len(
                value[1]
            ),
            reverse=True
        )

        for brand, alias in aliases:
            if cls._contains_phrase(
                text,
                alias
            ):
                return brand

        return ""

    @classmethod
    def _extract_by_category(
        cls,
        text,
        category
    ):
        markers = cls.CATEGORY_MARKERS.get(
            category,
            []
        )

        if markers:
            candidate = (
                cls._extract_before_markers(
                    text,
                    markers
                )
            )

            if candidate:
                return candidate

        if category == "SOFTWARE":
            return cls._extract_software_brand(
                text
            )

        return ""

    @classmethod
    def _extract_hierarchical_brand(
        cls,
        text
    ):
        if ">" not in text:
            return ""

        candidate = text.split(
            ">",
            1
        )[0]

        candidate = cls._remove_end_markers(
            candidate
        )

        candidate = cls._clean_candidate(
            candidate
        )

        return cls._validate_candidate(
            candidate,
            max_words=7
        )

    @classmethod
    def _extract_before_markers(
        cls,
        text,
        markers
    ):
        earliest = None

        for marker in markers:
            normalized_marker = (
                cls._normalize(marker)
            )

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(normalized_marker)
                + r"(?![a-z0-9])"
            )

            match = re.search(
                pattern,
                text
            )

            if not match:
                continue

            if match.start() == 0:
                continue

            if (
                earliest is None
                or match.start() < earliest
            ):
                earliest = match.start()

        if earliest is None:
            return ""

        candidate = text[
            :earliest
        ]

        candidate = cls._remove_trailing_variant(
            candidate
        )

        candidate = cls._clean_candidate(
            candidate
        )

        return cls._validate_candidate(
            candidate,
            max_words=7
        )

    @classmethod
    def _extract_before_dash(
        cls,
        text
    ):
        match = re.search(
            r"\s+-\s+",
            text
        )

        if not match:
            return ""

        left = text[
            :match.start()
        ].strip()

        right = text[
            match.end():
        ].strip()

        left = cls._clean_candidate(
            left
        )

        if not left:
            return ""

        words = left.split()

        if len(words) > 7:
            return ""

        if not cls._looks_like_variant(
            right
        ):
            return ""

        return cls._validate_candidate(
            left,
            max_words=7
        )

    @classmethod
    def _extract_software_brand(
        cls,
        text
    ):
        dash = re.search(
            r"\s+-\s+",
            text
        )

        if dash:
            left = cls._clean_candidate(
                text[:dash.start()]
            )

            if left:
                words = left.split()

                if 1 <= len(words) <= 4:
                    return left

        return ""

    @classmethod
    def _fallback_brand(
        cls,
        text
    ):
        candidate = text

        candidate = cls._strip_parenthetical_suffixes(
            candidate
        )

        candidate = cls._remove_money(
            candidate
        )

        candidate = cls._remove_quantity(
            candidate
        )

        candidate = cls._remove_duration(
            candidate
        )

        candidate = cls._remove_devices(
            candidate
        )

        candidate = cls._remove_regions(
            candidate
        )

        candidate = cls._remove_platforms(
            candidate
        )

        candidate = cls._remove_stores(
            candidate
        )

        candidate = cls._remove_generic_suffixes(
            candidate
        )

        candidate = cls._clean_candidate(
            candidate
        )

        candidate = cls._collapse_repeated_sequence(
            candidate
        )

        candidate = cls._clean_candidate(
            candidate
        )

        if not candidate:
            return ""

        words = candidate.split()

        if len(words) > 5:
            return ""

        if re.search(
            r"\d",
            candidate
        ):
            return ""

        if cls._contains_variant_word(
            candidate
        ):
            return ""

        return cls._validate_candidate(
            candidate,
            max_words=5
        )

    @classmethod
    def _looks_like_variant(
        cls,
        text
    ):
        if not text:
            return False

        if re.search(
            r"\d",
            text
        ):
            return True

        if re.search(
            rf"\b(?:{cls.CURRENCIES})\b",
            text
        ):
            return True

        for word in cls.VARIANT_WORDS:
            if cls._contains_phrase(
                text,
                word
            ):
                return True

        for pattern in cls.PLATFORM_PATTERNS:
            if re.search(
                pattern,
                text
            ):
                return True

        for pattern in cls.STORE_SUFFIXES:
            if re.search(
                pattern,
                text
            ):
                return True

        return False

    @classmethod
    def _remove_end_markers(
        cls,
        text
    ):
        result = text

        marker_pattern = (
            r"\s+("
            r"accounts?|"
            r"items?|"
            r"boosting|"
            r"boost|"
            r"currency|"
            r"services?|"
            r"top[\s-]?ups?"
            r")\s*$"
        )

        result = re.sub(
            marker_pattern,
            "",
            result
        )

        return result.strip()

    @classmethod
    def _remove_trailing_variant(
        cls,
        text
    ):
        result = text

        result = cls._remove_money(
            result
        )

        result = cls._remove_quantity(
            result
        )

        result = cls._remove_duration(
            result
        )

        result = cls._remove_devices(
            result
        )

        result = cls._remove_regions(
            result
        )

        result = cls._remove_platforms(
            result
        )

        result = cls._remove_stores(
            result
        )

        return result

    @classmethod
    def _remove_money(
        cls,
        text
    ):
        result = text

        result = re.sub(
            r"[$€£₹¥]\s*\d+(?:[.,]\d+)?",
            " ",
            result
        )

        result = re.sub(
            r"\d+(?:[.,]\d+)?\s*[$€£₹¥]",
            " ",
            result
        )

        result = re.sub(
            rf"\b\d+(?:[.,]\d+)?\s*"
            rf"(?:{cls.CURRENCIES})\b",
            " ",
            result
        )

        result = re.sub(
            rf"\b(?:{cls.CURRENCIES})\s*"
            rf"\d+(?:[.,]\d+)?\b",
            " ",
            result
        )

        return result

    @staticmethod
    def _remove_quantity(
        text
    ):
        return re.sub(
            (
                r"\b\d[\d\s.,]*\s*"
                r"(?:"
                r"rp|"
                r"uc|"
                r"cp|"
                r"points?|"
                r"coins?|"
                r"credits?|"
                r"robux|"
                r"v[\s-]?bucks|"
                r"gold|"
                r"gems?|"
                r"bonds?|"
                r"diamonds?|"
                r"tokens?|"
                r"jade|"
                r"crystals?|"
                r"platinum|"
                r"shards?"
                r")\b"
            ),
            " ",
            text
        )

    @staticmethod
    def _remove_duration(
        text
    ):
        return re.sub(
            (
                r"\b\d+\s*"
                r"(?:"
                r"hours?|"
                r"days?|"
                r"weeks?|"
                r"months?|"
                r"years?"
                r")\b"
            ),
            " ",
            text
        )

    @staticmethod
    def _remove_devices(
        text
    ):
        return re.sub(
            r"\b\d+\s*devices?\b",
            " ",
            text
        )

    @classmethod
    def _remove_regions(
        cls,
        text
    ):
        result = text

        for pattern in cls.REGION_PATTERNS:
            result = re.sub(
                pattern,
                " ",
                result
            )

        return result

    @classmethod
    def _remove_platforms(
        cls,
        text
    ):
        result = text

        for pattern in cls.PLATFORM_PATTERNS:
            result = re.sub(
                pattern,
                " ",
                result
            )

        return result

    @classmethod
    def _remove_stores(
        cls,
        text
    ):
        result = text

        for pattern in cls.STORE_SUFFIXES:
            result = re.sub(
                pattern,
                " ",
                result
            )

        return result

    @classmethod
    def _remove_generic_suffixes(
        cls,
        text
    ):
        result = text

        patterns = [
            r"\be-?gift cards?\b",
            r"\bgift cards?\b",
            r"\bgiftcard\b",

            r"\bprepaid cards?\b",
            r"\bvouchers?\b",

            r"\bactivation keys?\b",
            r"\bdigital keys?\b",
            r"\bcd keys?\b",
            r"\bkeys?\b",
            r"\bcodes?\b",

            r"\bsubscriptions?\b",
            r"\bmemberships?\b",

            r"\baccounts?\b",
            r"\bitems?\b",

            r"\btop[\s-]?ups?\b",

            r"\bboosting\b",
            r"\bboost\b",

            r"\bplayer trade\b",

            r"\bdirect\b",
            r"\bdigital\b",
            r"\bonline\b",
            r"\binstant\b",

            r"\bpackages?\b",
            r"\bbundles?\b",
            r"\bpacks?\b",

            r"\bgift bags?\b",

            r"\bactivation passes?\b",
            r"\bbattle passes?\b",
            r"\bpremium passes?\b",

            r"\bstandard editions?\b",
            r"\bdeluxe editions?\b",
            r"\bultimate editions?\b",
        ]

        for pattern in patterns:
            result = re.sub(
                pattern,
                " ",
                result
            )

        return result

    @staticmethod
    def _strip_parenthetical_suffixes(
        text
    ):
        return re.sub(
            r"\([^)]*\)",
            " ",
            text
        )

    @classmethod
    def _contains_variant_word(
        cls,
        text
    ):
        for word in cls.VARIANT_WORDS:
            if cls._contains_phrase(
                text,
                word
            ):
                return True

        return False

    @classmethod
    def _clean_candidate(
        cls,
        text
    ):
        value = text.lower()

        value = value.replace(
            "_",
            " "
        )

        value = value.replace(
            "–",
            "-"
        )

        value = value.replace(
            "—",
            "-"
        )

        value = re.sub(
            r"[|/]+",
            " ",
            value
        )

        value = re.sub(
            r"[()[\]{}]+",
            " ",
            value
        )

        value = re.sub(
            r"\s*-\s*-\s*",
            " ",
            value
        )

        value = re.sub(
            r"\s+",
            " ",
            value
        )

        value = value.strip(
            " -,:;>"
        )

        return cls._display_name(
            value
        )

    @classmethod
    def _validate_candidate(
        cls,
        candidate,
        max_words=7
    ):
        if not candidate:
            return ""

        normalized = cls._normalize(
            candidate
        )

        if not normalized:
            return ""

        invalid = {
            "account",
            "accounts",
            "item",
            "items",
            "boost",
            "boosting",
            "gift card",
            "gift cards",
            "subscription",
            "membership",
            "top up",
            "service",
            "services",
            "unknown",
            "digital",
            "direct",
            "global",
            "package",
            "bundle",
            "key",
            "code",
            "voucher",
        }

        if normalized in invalid:
            return ""

        if len(normalized) < 2:
            return ""

        if len(
            normalized.split()
        ) > max_words:
            return ""

        if re.fullmatch(
            r"[\d.,]+",
            normalized
        ):
            return ""

        return cls._display_name(
            normalized
        )

    @staticmethod
    def _collapse_repeated_sequence(
        text
    ):
        words = text.split()

        length = len(words)

        if length < 2:
            return text

        for size in range(
            1,
            (length // 2) + 1
        ):
            if length % size != 0:
                continue

            base = [
                word.lower()
                for word in words[:size]
            ]

            repetitions = (
                length // size
            )

            valid = True

            for index in range(
                1,
                repetitions
            ):
                current = [
                    word.lower()
                    for word in words[
                        index * size:
                        (index + 1) * size
                    ]
                ]

                if current != base:
                    valid = False
                    break

            if valid:
                return " ".join(
                    words[:size]
                )

        return text

    @staticmethod
    def _contains_phrase(
        text,
        phrase
    ):
        if not text or not phrase:
            return False

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(phrase)
            + r"(?![a-z0-9])"
        )

        return bool(
            re.search(
                pattern,
                text
            )
        )

    @staticmethod
    def _display_name(
        text
    ):
        special_words = {
            "pc": "PC",
            "ios": "iOS",

            "ea": "EA",
            "avg": "AVG",

            "vmware": "VMware",
            "winrar": "WinRAR",

            "paypal": "PayPal",
            "playstation": "PlayStation",

            "battle.net": "Battle.net",

            "lego": "LEGO",

            "h&m": "H&M",

            "tk": "TK",

            "tiktok": "TikTok",

            "bitjem": "BitJem",
            "cryptonow": "Cryptonow",

            "f-secure": "F-Secure",

            "osrs": "OSRS",
            "pubg": "PUBG",

            "arc": "ARC",

            "magix": "MAGIX",
            "iobit": "IObit",
            "minitool": "MiniTool",
            "cyberlink": "CyberLink",

            "ffxiv": "FFXIV",
            "smite": "SMITE",
        }

        lowercase_words = {
            "of",
            "the",
            "and",
            "for",
            "vs",
            "du",
        }

        result = []

        for index, word in enumerate(
            text.split()
        ):
            lower = word.lower()

            if lower in special_words:
                result.append(
                    special_words[lower]
                )
                continue

            if (
                index > 0
                and lower in lowercase_words
            ):
                result.append(
                    lower
                )
                continue

            result.append(
                word[:1].upper()
                + word[1:]
            )

        return " ".join(
            result
        )