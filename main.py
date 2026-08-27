import time

import pandas as pd

from mapper import ProductMapper


INPUT_FILE = "unmatched_offers.csv"

OUTPUT_TITLES = "titles_rest.csv"
OUTPUT_MAPPING = "offer_mapping.csv"
OUTPUT_REVIEW = "offers_to_review.csv"


def main():
    start_time = time.time()

    print(
        "Wczytywanie pliku..."
    )

    df = pd.read_csv(
        INPUT_FILE,
        sep=";",
        dtype=str,
        keep_default_na=False
    )

    print(
        f"Wczytano {len(df)} ofert."
    )

    mapper = ProductMapper()

    df = mapper.process(
        df
    )

    review = df[
        df["detected_category"]
        == "OTHER"
    ].copy()

    existing_pipeline = df[
        df["detected_category"]
        == "EXISTING_PIPELINE"
    ].copy()

    titles, offer_mapping = (
        mapper.build_titles(
            df
        )
    )

    print(
        "Zapisywanie wyników..."
    )

    titles.to_csv(
        OUTPUT_TITLES,
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    offer_mapping.to_csv(
        OUTPUT_MAPPING,
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    review.to_csv(
        OUTPUT_REVIEW,
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    elapsed = (
        time.time()
        - start_time
    )

    print()

    print(
        "===== WYNIKI ====="
    )

    print(
        "Wszystkie oferty:",
        len(df)
    )

    print(
        "Rozpoznane:",
        len(df) - len(review)
    )

    print(
        "Do ręcznej analizy:",
        len(review)
    )

    print(
        "Obsługiwane przez istniejący pipeline:",
        len(existing_pipeline)
    )

    print(
        "Utworzone produkty:",
        len(titles)
    )

    print()

    print(
        "Kategorie:"
    )

    print(
        df[
            "detected_category"
        ].value_counts()
    )

    print()

    print(
        "Najczęściej używane reguły:"
    )

    print(
        df[
            "match_rule"
        ]
        .value_counts()
        .head(30)
    )

    print()

    print(
        "===== ANALIZA OTHER ====="
    )

    print()

    print(
        "Najczęstsze feed_category w OTHER:"
    )

    if "feed_category" in review.columns:
        print(
            review[
                "feed_category"
            ]
            .value_counts()
            .head(20)
        )

    print()

    print(
        "Najczęstsze category w OTHER:"
    )

    if "category" in review.columns:
        print(
            review[
                "category"
            ]
            .value_counts()
            .head(20)
        )

    print()

    print(
        "Najczęstsze DRM w OTHER:"
    )

    if "drm" in review.columns:
        print(
            review[
                "drm"
            ]
            .value_counts()
            .head(20)
        )

    print()

    print(
        f"Czas wykonania: "
        f"{elapsed:.2f} s"
    )


if __name__ == "__main__":
    main()