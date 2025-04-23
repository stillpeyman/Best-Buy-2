import pytest

import promotions
from products import Product, NonStockedProduct, LimitedProduct
from promotions import PercentDiscount, SecondHalfPrice, ThirdOneFree, Promotion


def test_product_initialization():
    """
    Test proper initialization of a standard Product.
    """
    p = Product("Laptop", price=1200.50, quantity=10, promotions=None)
    assert p.name == "Laptop"
    assert p.price == 1200.50
    assert p.quantity == 10
    assert p.is_active is True
    assert p.promo == []


@pytest.mark.parametrize(
    "name, price, quantity",
    [
        ("", 1200.5, 10),
        ("Laptop", -50.0, 10),
        ("Laptop", 1200.5, -5)
    ]
)
def test_invalid_initialization(name, price, quantity):
    """
    Test that invalid name, price, or quantity raises an exception.
    """
    with pytest.raises(Exception):
        Product(name, price, quantity, promotions=None)


def test_price_getter():
    """
    Test the price getter returns the correct value.
    """
    p = Product("Laptop", price=1200.50, quantity=10)
    assert p.price == 1200.50


def test_price_setter():
    """
    Test setting a valid new price updates the product price.
    """
    p = Product("Laptop", price=1200.50, quantity=10)
    p.price = 1500.00
    assert p.price == 1500.00


def test_invalid_price():
    """
    Test setting an invalid price raises an exception.
    """
    p = Product("Laptop", price=1200.50, quantity=10)
    with pytest.raises(Exception):
        p.price = -100
    with pytest.raises(Exception):
        p.price = "invalid"


def test_quantity():
    """
    Test initial quantity is set correctly.
    """
    p = Product("Phone", price=800.0, quantity=5)
    assert p.quantity == 5


def test_set_quantity():
    """
    Test setting quantity and resulting is_active status.
    """
    p = Product("Tablet", price=300.0, quantity=5)

    p.quantity = 10
    assert p.quantity == 10

    p.quantity = 0
    assert p.quantity == 0
    assert p.is_active is False


@pytest.mark.parametrize("invalid_quantity", ["20", -1])
def test_set_quantity_invalid(invalid_quantity):
    """
    Test setting invalid quantity (non-int or negative) raises an exception.
    """
    p = Product("Tablet", price=300.0, quantity=5)
    with pytest.raises(Exception):
        p.quantity(invalid_quantity)


def test_update_quantity():
    """
    Test reducing quantity and automatic deactivation when reaching 0.
    """
    p = Product("Tablet", price=300.0, quantity=5)

    p.update_quantity(4)
    assert p.quantity == 1
    assert p.is_active is True

    p.update_quantity(1)
    assert p.quantity == 0
    assert p.is_active is False


@pytest.mark.parametrize("invalid_quantity", ["20", -1, 10])
def test_update_invalid_quantity(invalid_quantity):
    """
    Test updating quantity with invalid value raises an exception.
    """
    p = Product("Tablet", price=300.0, quantity=5)
    with pytest.raises(Exception):
        p.update_quantity(invalid_quantity)


def test_buy():
    """
    Test purchasing a product correctly updates quantity and returns total cost.
    """
    p = Product("Monitor", price=200.0, quantity=10)
    assert p.buy(2) == 400.0
    assert p.quantity == 8


@pytest.mark.parametrize("invalid_quantity", [0, 20, -1])
def test_buy_invalid_quantity(invalid_quantity):
    """
    Test buying with invalid quantity (0, too much, negative) raises an exception.
    """
    p = Product("Monitor", price=200.0, quantity=10)
    with pytest.raises(Exception):
        p.buy(invalid_quantity)


@pytest.mark.parametrize("promo_list", [
    [promotions.SecondHalfPrice("Second Half Price"),
     promotions.ThirdOneFree("Third One Free"),
     promotions.PercentDiscount("30% off", 30)]
])
def test_add_promo(promo_list):
    """
    Test adding multiple promotions to a product.
    """
    p = Product("Monitor", price=200.0, quantity=10)
    p.add_promo(promo_list)

    # check that all promos are added
    assert all(promo in p.promo for promo in promo_list)
    assert len(p.promo) == len(promo_list)


@pytest.mark.parametrize("promo_list", [
    [promotions.SecondHalfPrice("Second Half Price"),
     promotions.ThirdOneFree("Third One Free"),
     promotions.PercentDiscount("30% off", 30)]
])
def test_remove_promo(promo_list):
    """
    Test removing a specific promotion from the product.
    """
    p = Product("Monitor", price=200.0, quantity=10)
    p.add_promo(promo_list)

    # remove one promo
    p.remove_promo(promo_list[1])

    assert promo_list[1] not in p.promo
    assert len(p.promo) == len(promo_list) - 1


def test_status():
    """
    Test product deactivation when quantity hits zero after a purchase.
    """
    p = Product("Keyboard", price=50.0, quantity=1)
    # Initially active
    assert p.is_active is True

    # Reduce quantity to 0
    p.buy(1)
    # Should now be inactive
    assert p.is_active is False


def test_activation():
    """
    Test manual activation and deactivation of product status.
    """
    p = Product("Mouse", price=30.0, quantity=10)
    p.deactivate()
    assert p.is_active is False

    p.activate()
    assert p.is_active is True


# Test NonStockedProduct
def test_non_stocked_product_init():
    """
    Test initialization of a NonStockedProduct.
    """
    p = NonStockedProduct("Windows License", price=100.00)
    assert p.name == "Windows License"
    assert p.price == 100.00
    assert p.quantity == 0
    assert p.is_active is True

    p_inactive = NonStockedProduct("Windows License", price=100.00, is_active=False)
    assert p_inactive._is_active is False


def test_non_stocked_product_buy():
    """
    Test purchase behavior for NonStockedProduct (no quantity reduction).
    """
    p = NonStockedProduct("Windows License", price=100)
    assert p.buy(1) == 100
    assert p.buy(3) == 300
    assert p.quantity == 0


@pytest.mark.parametrize("invalid_quantity", ["20", -1])
def test_non_stocked_product_buy_invalid_quantity(invalid_quantity):
    """
    Test buying NonStockedProduct with invalid quantity raises an exception.
    """
    p = NonStockedProduct("Windows License", price=100)
    with pytest.raises(Exception):
        # Purchase quantity must be int
        p.buy(invalid_quantity)


def test_non_stocked_product_buy_inactive():
    """
    Test buying inactive NonStockedProduct raises an exception.
    """
    p_inactive = NonStockedProduct("Windows License", price=100.00, is_active=False)
    with pytest.raises(Exception):
        # Trying to buy unavailable product
        p_inactive.buy(1)


def test_limited_product_init():
    """
    Test LimitedProduct initializes with max_quantity limit.
    """
    p = LimitedProduct("Shipping", price=10, quantity=250, max_quantity=1)
    assert p.name == "Shipping"
    assert p.price == 10.00
    assert p.quantity == 250
    assert p.max_quantity == 1
    assert p.is_active is True


def test_limited_product_buy():
    """
    Test buying a LimitedProduct with valid quantity.
    """
    p = LimitedProduct("Shipping", price=10, quantity=250, max_quantity=1)
    assert p.buy(1) == 10
    assert p.quantity == 249


@pytest.mark.parametrize("invalid_quantity", [5, "5", -1])
def test_limited_product_buy_invalid_quantity(invalid_quantity):
    """
    Test LimitedProduct rejects invalid or excessive purchase quantities.
    """
    p = LimitedProduct("Shipping", price=10, quantity=250, max_quantity=1)
    with pytest.raises(Exception):
        p.buy(invalid_quantity)


def test_product_comparison_lt():
    """
    Test less-than comparison between products by price.
    """
    p1 = Product("Monitor", price=200.0, quantity=10)
    p2 = Product("Phone", price=800.0, quantity=5)

    assert p1 < p2
    assert not (p2 < p1)
    assert not (p1 < p1)


def test_product_comparison_gt():
    """
    Test greater-than comparison between products by price.
    """
    p1 = Product("Monitor", price=1000.0, quantity=10)
    p2 = Product("Phone", price=800.0, quantity=5)

    assert p1 > p2
    assert not (p2 > p1)
    assert not (p1 > p1)


def test_product_comparison_with_non_product():
    """
    Test product comparison with non-product object raises exception.
    """
    p = Product("Monitor", price=1000.0, quantity=10)

    with pytest.raises(Exception):
        p < "Not a Product"

    with pytest.raises(Exception):
        p > "Not a Product"




