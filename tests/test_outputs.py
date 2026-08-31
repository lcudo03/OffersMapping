import pandas as pd


TITLES_FILE = "titles_rest.csv"
MAPPING_FILE = "offer_mapping.csv"


def load_titles():
    return pd.read_csv(
        TITLES_FILE,
        sep=";",
        dtype=str,
        keep_default_na=False
    )


def load_mapping():
    return pd.read_csv(
        MAPPING_FILE,
        sep=";",
        dtype=str,
        keep_default_na=False
    )


def test_title_ids_are_unique():
    titles = load_titles()

    assert not titles["id"].duplicated().any()


def test_skeleton_keys_are_unique():
    titles = load_titles()

    assert not titles["skeleton_key"].duplicated().any()


def test_slugs_are_unique():
    titles = load_titles()

    assert not titles["slug"].duplicated().any()


def test_names_are_not_empty():
    titles = load_titles()

    empty_names = (
        titles["name"]
        .astype(str)
        .str.strip()
        .eq("")
    )

    assert not empty_names.any()


def test_skeleton_keys_are_not_empty():
    titles = load_titles()

    empty_keys = (
        titles["skeleton_key"]
        .astype(str)
        .str.strip()
        .eq("")
    )

    assert not empty_keys.any()


def test_offer_ids_are_unique():
    mapping = load_mapping()

    assert not mapping["offer_id"].duplicated().any()


def test_all_mapping_titles_exist():
    titles = load_titles()
    mapping = load_mapping()

    title_ids = set(
        titles["id"]
    )

    mapped_ids = set(
        mapping["title_rest_id"]
    )

    missing_ids = (
        mapped_ids - title_ids
    )

    assert not missing_ids


def test_every_title_has_offer():
    titles = load_titles()
    mapping = load_mapping()

    title_ids = set(
        titles["id"]
    )

    mapped_ids = set(
        mapping["title_rest_id"]
    )

    unused_ids = (
        title_ids - mapped_ids
    )

    assert not unused_ids