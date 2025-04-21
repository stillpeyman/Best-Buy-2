import pytest
from promotions import PercentDiscount, SecondHalfPrice, ThirdOneFree, Promotion


class DummyProduct:
    """Simple dummy product for testing purposes."""
    def __init__(self, price):
        self.price = price


@pytest.mark.parametrize("price, quantity, percent, expected", [
    (100, 1, 20, 80.0),
    (100, 2, 50, 100.0),
    (200, 3, 10, 540.0)
])
def test_percent_discount(price, quantity, percent, expected):
    product = DummyProduct(price)
    promo = PercentDiscount("Test Percent", percent)
    assert promo.apply_promotion(product, quantity) == expected


@pytest.mark.parametrize("price, quantity, expected", [
    (100, 1, 100.0),
    (100, 2, 150.0),
    (100, 3, 250.0),
    (100, 4, 300.0),
    (50, 5, 200.0)
])
def test_second_half_price_even_quantity(price, quantity, expected):
    product = DummyProduct(price)
    promo = SecondHalfPrice("Test Second Half")
    assert promo.apply_promotion(product, quantity) == expected


@pytest.mark.parametrize("price, quantity, expected", [
    (100, 1, 100.0),
    (100, 2, 200.0),
    (100, 3, 200.0),
    (100, 4, 300.0),
    (100, 5, 400.0),
    (100, 6, 400.0),
    (100, 7, 500.0),
    (100, 8, 600.0),
    (100, 9, 600.0)
])
def test_third_one_free(price, quantity, expected):
    promo = ThirdOneFree("Test Third One Free")
    product = DummyProduct(price)
    assert promo.apply_promotion(product, quantity) == expected


def test_promo_str():
    promo = PercentDiscount("Black Friday", 50)
    assert str(promo) == "Black Friday"


def test_abstract_promo():
    class DummyPromotion(Promotion):
        pass
    with pytest.raises(TypeError):
        DummyPromotion("Error")

