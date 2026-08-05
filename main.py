import pandas as pd
import re
import unicodedata


INPUT_FILE = "unmatched_offers.csv"
OUTPUT_FILE = "titles_rest.csv"


def normalize(text):
    if pd.isna(text):
        return ""

    text = str(text).lower().strip()

    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        c for c in text
        if not unicodedata.combining(c)
    )

    text = re.sub(r"\s+", " ", text)

    return text


def slugify(text):
    text = normalize(text)

    text = re.sub(
        r"[^a-z0-9]+",
        "-",
        text
    )

    return text.strip("-")


def detect_category(row):
    name = normalize(row["clean_name"])
    feed_category = normalize(row["feed_category"])


    if "ingame_currency" in feed_category:
        return "IN_GAME_CURRENCY"

    if "ingame_item" in feed_category:
        return "IN_GAME_ITEM"

    if "software" in feed_category:
        return "SOFTWARE"

    if "gift" in feed_category:
        return "GIFT_CARD"

    if "prepaid" in feed_category:
        return "GIFT_CARD"

    if "topup" in feed_category:
        return "TOP_UP"


    if any(x in name for x in [
        "gift card",
        "giftcard",
        "wallet card",
        "voucher"
    ]):
        return "GIFT_CARD"

    if any(x in name for x in [
        "v-bucks",
        "v bucks",
        "robux",
        "fc points",
        "riot points"
    ]):
        return "IN_GAME_CURRENCY"

    if any(x in name for x in [
        "game pass",
        "ps plus",
        "playstation plus",
        "subscription"
    ]):
        return "SUBSCRIPTION"

    if any(x in name for x in [
        "windows",
        "office",
        "antivirus",
        "internet security",
        "vpn"
    ]):
        return "SOFTWARE"

    return "OTHER"


def create_skeleton_key(row):
    """
    Na razie prosta wersja.
    """

    name = normalize(row["clean_name"])

    remove_words = [
        "global",
        "key",
        "cd key"
    ]

    for word in remove_words:
        name = name.replace(word, "")

    name = re.sub(r"\s+", " ", name).strip()

    category = detect_category(row)

    return slugify(
        f"{category}-{name}"
    )


df = pd.read_csv(
    INPUT_FILE,
    sep=";",
    dtype=str,
    keep_default_na=False
)


print("Liczba ofert:", len(df))


df["detected_category"] = df.apply(
    detect_category,
    axis=1
)

df["skeleton_key_new"] = df.apply(
    create_skeleton_key,
    axis=1
)


# group

grouped = (
    df[df["detected_category"] != "OTHER"]
    .groupby("skeleton_key_new", as_index=False)
    .first()
)


titles_rest = pd.DataFrame({
    "id": range(1, len(grouped) + 1),

    "name":
        grouped["clean_name"],

    "slug":
        grouped["clean_name"].apply(slugify),

    "skeleton_key":
        grouped["skeleton_key_new"],

    "image_url":
        grouped["image_url"],

    "category":
        grouped["detected_category"],

    "edition":
        grouped["edition"],

    "system_id":
        grouped["drm"]
})


titles_rest.to_csv(
    OUTPUT_FILE,
    sep=";",
    index=False
)


print(
    "Utworzono produktów:",
    len(titles_rest)
)

print(
    "Zapisano:",
    OUTPUT_FILE
)