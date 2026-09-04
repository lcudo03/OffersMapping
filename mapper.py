import pandas as pd

from brand_detector import BrandDetector
from classifier import ProductClassifier
from extractors import ProductExtractor
from key_builder import SkeletonKeyBuilder
from normalizer import TextNormalizer


class ProductMapper:

    def __init__(self):
        self.classifier = ProductClassifier()
        self.key_builder = SkeletonKeyBuilder()

    def process(self, df):
        print(
            "Klasyfikacja produktów..."
        )

        classification = df.apply(
            self.classifier.classify,
            axis=1
        )

        df["detected_category"] = [
            result[0]
            for result in classification
        ]

        df["confidence"] = [
            result[1]
            for result in classification
        ]

        df["match_rule"] = [
            result[2]
            for result in classification
        ]

        print(
            "Wykrywanie regionów..."
        )

        df["detected_region"] = df.apply(
            ProductExtractor.detect_region,
            axis=1
        )

        print(
            "Wykrywanie platform..."
        )

        df["detected_platform"] = df.apply(
            ProductExtractor.detect_platform,
            axis=1
        )

        print(
            "Wykrywanie brandów..."
        )

        df["detected_brand"] = df.apply(
            BrandDetector.detect,
            axis=1
        )

        df["brand_key"] = (
            df["detected_brand"]
            .apply(
                BrandDetector.canonical_key
            )
        )

        print(
            "Budowanie skeleton_key..."
        )

        df["new_skeleton_key"] = df.apply(
            self.key_builder.create,
            axis=1
        )

        return df

    def build_titles(self, df):
        matched = df[
            ~df["detected_category"].isin(
                [
                    "OTHER",
                    "EXISTING_PIPELINE"
                ]
            )
        ].copy()

        grouped = matched.groupby(
            "new_skeleton_key",
            sort=False
        )

        temporary_products = []
        temporary_mapping = []

        product_id = 1

        for skeleton_key, group in grouped:
            first = group.iloc[0]

            product_name = (
                self._choose_product_name(
                    group
                )
            )

            product_slug = (
                TextNormalizer.slugify(
                    skeleton_key
                )
            )

            brand_name = (
                self._choose_brand(
                    group
                )
            )

            brand_key = (
                BrandDetector.canonical_key(
                    brand_name
                )
            )

            temporary_products.append(
                {
                    "id": product_id,
                    "name": product_name,
                    "slug": product_slug,
                    "skeleton_key": skeleton_key,
                    "image_url": self._choose_image(
                        group
                    ),
                    "category": first[
                        "detected_category"
                    ],
                    "edition": first.get(
                        "edition",
                        ""
                    ),
                    "brand_name": brand_name,
                    "brand_key": brand_key,
                }
            )

            for _, offer in group.iterrows():
                offer_brand = offer[
                    "detected_brand"
                ]

                offer_brand_key = (
                    BrandDetector.canonical_key(
                        offer_brand
                    )
                )

                temporary_mapping.append(
                    {
                        "offer_id": offer["id"],
                        "title_rest_id": (
                            product_id
                        ),
                        "skeleton_key": (
                            skeleton_key
                        ),
                        "category": offer[
                            "detected_category"
                        ],
                        "platform": offer[
                            "detected_platform"
                        ],
                        "region": offer[
                            "detected_region"
                        ],
                        "brand_name": (
                            offer_brand
                        ),
                        "brand_key": (
                            offer_brand_key
                        ),
                        "confidence": offer[
                            "confidence"
                        ],
                        "match_rule": offer[
                            "match_rule"
                        ],
                    }
                )

            product_id += 1

        products_df = pd.DataFrame(
            temporary_products
        )

        mapping_df = pd.DataFrame(
            temporary_mapping
        )

        brands = self._build_brands(
            products_df
        )

        brand_id_by_key = dict(
            zip(
                brands["brand_key"],
                brands["id"]
            )
        )

        products_df["brand_id"] = (
            products_df["brand_key"]
            .map(
                brand_id_by_key
            )
        )

        mapping_df["brand_id"] = (
            mapping_df["brand_key"]
            .map(
                brand_id_by_key
            )
        )

        products_df = products_df.drop(
            columns=[
                "brand_name",
                "brand_key",
            ]
        )

        mapping_df = mapping_df.drop(
            columns=[
                "brand_name",
                "brand_key",
            ]
        )

        brands = brands.drop(
            columns=[
                "brand_key"
            ]
        )

        products_df = products_df[
            [
                "id",
                "name",
                "slug",
                "skeleton_key",
                "image_url",
                "category",
                "edition",
                "brand_id",
            ]
        ]

        return (
            products_df,
            mapping_df,
            brands
        )

    @staticmethod
    def _build_brands(
        products
    ):
        if products.empty:
            return pd.DataFrame(
                columns=[
                    "id",
                    "name",
                    "slug",
                    "brand_key",
                ]
            )

        source = products[
            [
                "brand_name",
                "brand_key"
            ]
        ].copy()

        source["brand_name"] = (
            source["brand_name"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

        source["brand_key"] = (
            source["brand_key"]
            .fillna("unknown")
            .astype(str)
            .str.strip()
        )

        source.loc[
            source["brand_name"] == "",
            "brand_name"
        ] = "Unknown"

        source.loc[
            source["brand_key"] == "",
            "brand_key"
        ] = "unknown"

        brand_rows = []

        grouped = source.groupby(
            "brand_key",
            sort=True
        )

        for brand_key, group in grouped:
            names = (
                group["brand_name"]
                .value_counts()
            )

            if brand_key == "unknown":
                display_name = "Unknown"
            else:
                display_name = (
                    ProductMapper
                    ._choose_brand_display_name(
                        names
                    )
                )

            brand_rows.append(
                {
                    "name": display_name,
                    "slug": brand_key,
                    "brand_key": brand_key,
                }
            )

        brand_rows.sort(
            key=lambda row: row[
                "slug"
            ]
        )

        for index, row in enumerate(
            brand_rows,
            start=1
        ):
            row["id"] = index

        brands = pd.DataFrame(
            brand_rows
        )

        brands = brands[
            [
                "id",
                "name",
                "slug",
                "brand_key",
            ]
        ]

        return brands

    @staticmethod
    def _choose_brand_display_name(
        counts
    ):

        candidates = list(
            counts.index
        )

        candidates = [
            value
            for value in candidates
            if (
                value
                and value != "Unknown"
            )
        ]

        if not candidates:
            return "Unknown"

        def score(value):
            penalty = 0

            penalty += (
                value.count(">")
                * 100
            )

            penalty += (
                value.count("|")
                * 100
            )

            penalty += (
                value.count("--")
                * 100
            )

            if "&" in value:
                penalty -= 5

            frequency = counts.get(
                value,
                0
            )

            return (
                penalty,
                -frequency,
                len(value),
                value.lower(),
            )

        return min(
            candidates,
            key=score
        )

    @staticmethod
    def _choose_brand(
        group
    ):
        brands = (
            group["detected_brand"]
            .dropna()
            .astype(str)
            .str.strip()
        )

        brands = brands[
            brands != ""
        ]

        if brands.empty:
            return "Unknown"

        keys = brands.apply(
            BrandDetector.canonical_key
        )

        key_counts = (
            keys.value_counts()
        )

        winning_key = (
            key_counts.index[0]
        )

        candidates = brands[
            keys == winning_key
        ]

        if candidates.empty:
            return "Unknown"

        counts = (
            candidates.value_counts()
        )

        return (
            ProductMapper
            ._choose_brand_display_name(
                counts
            )
        )

    @staticmethod
    def _choose_product_name(
        group
    ):
        names = (
            group["clean_name"]
            .dropna()
            .astype(str)
            .str.strip()
        )

        names = names[
            names != ""
        ].tolist()

        if not names:
            return ""

        names.sort(
            key=lambda value: (
                len(value),
                value.lower()
            )
        )

        return names[0]

    @staticmethod
    def _choose_image(
        group
    ):
        if (
            "image_url"
            not in group.columns
        ):
            return ""

        images = (
            group["image_url"]
            .dropna()
            .astype(str)
            .str.strip()
        )

        images = images[
            images != ""
        ]

        if images.empty:
            return ""

        return images.iloc[0]