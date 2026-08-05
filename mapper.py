import pandas as pd

from classifier import ProductClassifier
from extractors import ProductExtractor
from key_builder import SkeletonKeyBuilder
from normalizer import TextNormalizer


class ProductMapper:

    def __init__(self):
        self.classifier = ProductClassifier()
        self.key_builder = SkeletonKeyBuilder()

    def process(self, df):
        print("Klasyfikacja produktów...")

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

        print("Wykrywanie regionów...")

        df["detected_region"] = df.apply(
            ProductExtractor.detect_region,
            axis=1
        )

        print("Wykrywanie platform...")

        df["detected_platform"] = df.apply(
            ProductExtractor.detect_platform,
            axis=1
        )

        print("Budowanie skeleton_key...")

        df["new_skeleton_key"] = df.apply(
            self.key_builder.create,
            axis=1
        )

        return df

    def build_titles(self, df):
        matched = df[
            df["detected_category"] != "OTHER"
        ].copy()

        grouped = matched.groupby(
            "new_skeleton_key",
            sort=False
        )

        products = []
        mapping = []

        product_id = 1

        for skeleton_key, group in grouped:
            first = group.iloc[0]

            product_name = self._choose_product_name(
                group
            )

            product_slug = TextNormalizer.slugify(
                product_name
            )

            products.append(
                {
                    "id": product_id,
                    "name": product_name,
                    "slug": product_slug,
                    "skeleton_key": skeleton_key,
                    "image_url": first.get(
                        "image_url",
                        ""
                    ),
                    "category": first[
                        "detected_category"
                    ],
                    "edition": first.get(
                        "edition",
                        ""
                    ),
                    "system_id": "",
                }
            )

            for _, offer in group.iterrows():
                mapping.append(
                    {
                        "offer_id": offer["id"],
                        "title_rest_id": product_id,
                        "skeleton_key": skeleton_key,
                        "category": offer[
                            "detected_category"
                        ],
                        "platform": offer[
                            "detected_platform"
                        ],
                        "region": offer[
                            "detected_region"
                        ],
                        "confidence": offer[
                            "confidence"
                        ],
                        "match_rule": offer[
                            "match_rule"
                        ],
                    }
                )

            product_id += 1

        titles = pd.DataFrame(products)
        offer_mapping = pd.DataFrame(mapping)

        return titles, offer_mapping

    @staticmethod
    def _choose_product_name(group):
        names = (
            group["clean_name"]
            .dropna()
            .astype(str)
            .tolist()
        )

        if not names:
            return ""

        names.sort(key=len)

        return names[0]