from classifier import ProductClassifier


classifier = ProductClassifier()


def classify(**kwargs):
    row = {
        "clean_name": "",
        "original_name": "",
        "feed_category": "",
        "category": "",
        "drm": "",
    }

    row.update(kwargs)

    return classifier.classify(row)[0]


def test_steam_gift_is_existing_pipeline():
    result = classify(
        clean_name="Helldivers 2 Steam Gift",
        category="GAME_GIFT"
    )

    assert result == "EXISTING_PIPELINE"


def test_gift_card():
    result = classify(
        clean_name="PlayStation Gift Card 50 EUR"
    )

    assert result == "GIFT_CARD"


def test_crypto_voucher_before_gift_card():
    result = classify(
        clean_name="Rewarble Crypto USD 25 Gift Card"
    )

    assert result == "CRYPTO_VOUCHER"


def test_ingame_currency():
    result = classify(
        clean_name="Fortnite 2800 V-Bucks"
    )

    assert result == "IN_GAME_CURRENCY"


def test_game_account():
    result = classify(
        clean_name="EA Sports FC 26 Account",
        feed_category="INGAME_ACCOUNT"
    )

    assert result == "ACCOUNT"


def test_subscription():
    result = classify(
        clean_name="Xbox Game Pass Ultimate 3 Months"
    )

    assert result == "SUBSCRIPTION"


def test_software():
    result = classify(
        clean_name="Microsoft Office 2021 Professional Plus"
    )

    assert result == "SOFTWARE"


def test_ingame_item():
    result = classify(
        clean_name="Counter Strike 2 AK-47 Skin"
    )

    assert result == "IN_GAME_ITEM"


def test_nintendo_eshop_drm_does_not_make_game_gift_card():
    result = classify(
        clean_name="Pokemon Scarlet",
        category="GAME",
        drm="Nintendo eShop"
    )

    assert result == "EXISTING_PIPELINE"