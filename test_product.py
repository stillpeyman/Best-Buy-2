import pytest
from products import Product, NonStockedProduct, LimitedProduct


def test_product_initialization():
    p = Product("Laptop", price=1200.50, quantity=10)
    assert p.name == "Laptop"
    assert p.price == 1200.50
    assert p.quantity == 10
    assert p.is_active is True


def test_invalid_initialization():
    with pytest.raises(Exception):
        # Empty name
        Product("", price=1200.50, quantity=10)
    with pytest.raises(Exception):
        # Negative price
        Product("Laptop", price=-50.0, quantity=10)
    with pytest.raises(Exception):
        # Negative quantity
        Product("Laptop", price=1200.50, quantity=-5)


def test_get_quantity():
    p = Product("Phone", price=800.0, quantity=5)
    assert p.get_quantity() == 5


def test_set_quantity():
    p = Product("Tablet", price=300.0, quantity=5)

    # add 5
    p.set_quantity(5)
    assert p.get_quantity() == 10

    # add 0
    p.set_quantity(0)
    assert p.get_quantity() == 10
    assert p.get_status() is True

    with pytest.raises(Exception):
        # Not integer
        p.set_quantity("20")

    with pytest.raises(Exception):
        # Invalid quantity
        p.set_quantity(-1)


def test_buy():
    p = Product("Monitor", price=200.0, quantity=10)
    assert p.buy(2) == 400.0
    assert p.get_quantity() == 8

    with pytest.raises(Exception):
        # Not enough stock
        p.buy(20)

    with pytest.raises(Exception):
        # Invalid quantity
        p.buy(-1)


def test_status():
    p = Product("Keyboard", price=50.0, quantity=1)
    # Initially active
    assert p.get_status() is True

    # Reduce quantity to 0
    p.buy(1)
    # Should now be inactive
    assert p.get_status() is False


def test_activation():
    p = Product("Mouse", price=30.0, quantity=10)
    p.deactivate()
    assert p.get_status() is False

    p.activate()
    assert p.get_status() is True


# Test NonStockedProduct
def test_non_stocked_product_init():
    p = NonStockedProduct("Windows License", price=100.00)
    assert p.name == "Windows License"
    assert p.price == 100.00
    assert p.quantity == 0
    assert p.is_active is True

    p_inactive = NonStockedProduct("Windows License", price=100.00, is_active=False)
    assert p_inactive.is_active is False


def test_non_stocked_product_buy():
    p = NonStockedProduct("Windows License", price=100)
    assert p.buy(1) == 100
    assert p.buy(3) == 300
    assert p.get_quantity() == 0

    with pytest.raises(Exception):
        # Purchase quantity must be int
        p.buy("20")

    with pytest.raises(Exception):
        # Invalid quantity
        p.buy(-1)

    with pytest.raises(Exception):
        p_inactive = NonStockedProduct("Windows License", price=100.00, is_active=False)
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

    with pytest.raises(Exception):
        # Invalid quantity
        p.buy(5)

    with pytest.raises(Exception):
        # Purchase quantity must be int
        p.buy("5")

    with pytest.raises(Exception):
        # Invalid quantity
        p.buy(-1)



