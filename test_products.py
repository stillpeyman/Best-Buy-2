import pytest
from products import Product, NonStockedProduct, LimitedProduct


def test_product_initialization():
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
    with pytest.raises(Exception):
        Product(name, price, quantity, promotions=None)


def test_price_getter():
    p = Product("Laptop", price=1200.50, quantity=10)
    assert p.price == 1200.50


def test_price_setter():
    p = Product("Laptop", price=1200.50, quantity=10)
    p.price = 1500.00
    assert p.price == 1500.00


def test_invalid_price():
    p = Product("Laptop", price=1200.50, quantity=10)
    with pytest.raises(Exception):
        p.price = -100
    with pytest.raises(Exception):
        p.price = "invalid"


def test_quantity():
    p = Product("Phone", price=800.0, quantity=5)
    assert p.quantity == 5


def test_set_quantity():
    p = Product("Tablet", price=300.0, quantity=5)

    p.quantity = 10
    assert p.quantity == 10

    p.quantity = 0
    assert p.quantity == 0
    assert p.is_active is False


@pytest.mark.parametrize("invalid_quantity", ["20", -1])
def test_set_quantity_invalid(invalid_quantity):
    p = Product("Tablet", price=300.0, quantity=5)
    with pytest.raises(Exception):
        p.quantity(invalid_quantity)


def test_buy():
    p = Product("Monitor", price=200.0, quantity=10)
    assert p.buy(2) == 400.0
    assert p.quantity == 8


@pytest.mark.parametrize("invalid_quantity", [20, -1])
def test_buy_invalid_quantity(invalid_quantity):
    p = Product("Monitor", price=200.0, quantity=10)
    with pytest.raises(Exception):
        p.buy(invalid_quantity)


def test_status():
    p = Product("Keyboard", price=50.0, quantity=1)
    # Initially active
    assert p.is_active is True

    # Reduce quantity to 0
    p.buy(1)
    # Should now be inactive
    assert p.is_active is False


def test_activation():
    p = Product("Mouse", price=30.0, quantity=10)
    p.deactivate()
    assert p.is_active is False

    p.activate()
    assert p.is_active is True


# Test NonStockedProduct
def test_non_stocked_product_init():
    p = NonStockedProduct("Windows License", price=100.00)
    assert p.name == "Windows License"
    assert p.price == 100.00
    assert p.quantity == 0
    assert p.is_active is True

    p_inactive = NonStockedProduct("Windows License", price=100.00, is_active=False)
    assert p_inactive._is_active is False


def test_non_stocked_product_buy():
    p = NonStockedProduct("Windows License", price=100)
    assert p.buy(1) == 100
    assert p.buy(3) == 300
    assert p.quantity == 0


@pytest.mark.parametrize("invalid_quantity", ["20", -1])
def test_non_stocked_product_buy_invalid_quantity(invalid_quantity):
    p = NonStockedProduct("Windows License", price=100)
    with pytest.raises(Exception):
        # Purchase quantity must be int
        p.buy(invalid_quantity)


def test_non_stocked_product_buy_inactive():
    p_inactive = NonStockedProduct("Windows License", price=100.00, is_active=False)
    with pytest.raises(Exception):
        # Trying to buy unavailable product
        p_inactive.buy(1)


def test_limited_product_init():
    p = LimitedProduct("Shipping", price=10, quantity=250, max_quantity=1)
    assert p.name == "Shipping"
    assert p.price == 10.00
    assert p.quantity == 250
    assert p.max_quantity == 1
    assert p.is_active is True


def test_limited_product_buy():
    p = LimitedProduct("Shipping", price=10, quantity=250, max_quantity=1)
    assert p.buy(1) == 10
    assert p.quantity == 249


@pytest.mark.parametrize("invalid_quantity", [5, "5", -1])
def test_limited_product_buy_invalid_quantity(invalid_quantity):
    p = LimitedProduct("Shipping", price=10, quantity=250, max_quantity=1)
    with pytest.raises(Exception):
        p.buy(invalid_quantity)


def test_product_comparison_lt():
    p1 = Product("Monitor", price=200.0, quantity=10)
    p2 = Product("Phone", price=800.0, quantity=5)

    assert p1 < p2
    assert not (p2 < p1)
    assert not (p1 < p1)


def test_product_comparison_gt():
    p1 = Product("Monitor", price=1000.0, quantity=10)
    p2 = Product("Phone", price=800.0, quantity=5)

    assert p1 > p2
    assert not (p2 > p1)
    assert not (p1 > p1)


def test_product_comparison_with_non_product():
    p = Product("Monitor", price=1000.0, quantity=10)

    with pytest.raises(Exception):
        p < "Not a Product"

    with pytest.raises(Exception):
        p > "Not a Product"




