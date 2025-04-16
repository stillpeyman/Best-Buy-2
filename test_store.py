import pytest
from store import Store
from products import Product


"""
First, create a 'pytest' Fixture: a function to set up reusable test data before each test runs,
in this case here create a Store instance with some products to be used in every single test,
thus avoid code repetition/duplication, keep it clean and easy to maintain!
"""
@pytest.fixture
def sample_store():
    """Fixture to create sample Store instance with products"""
    product_list = [Product("MacBook Air M2", price=1450, quantity=100),
                    Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    Product("Google Pixel 7", price=500, quantity=250),
                    ]
    return Store(product_list)


def test_store_init(sample_store):
    """Test store init with valid product list"""
    # Store should have 3 products
    assert len(sample_store.product_list) == 3


def test_invalid_init():
    with pytest.raises(Exception):
        # Empty list should raise an exception
        Store([])

    with pytest.raises(Exception):
        # Tuple instead of list should raise an exception
        Store(("MacBook Air M2", 1450, 100))


def test_add_product(sample_store):
    """Test adding a new product"""
    new_product = Product("Sony Alpha 7", price=1700, quantity=10)
    sample_store.add_product(new_product)

    # Product should be added
    assert new_product in sample_store.product_list
    # Store should have 4 products
    assert len(sample_store.product_list) == 4


def test_add_invalid_product(sample_store):
    """Test adding invalid product (not a Product instance)"""
    with pytest.raises(Exception):
        # Should raise an exception
        sample_store.add_product("Not a product object")


def test_remove_product(sample_store):
    """Test removing a product that is not in the store"""
    fake_product = Product("Nonexistent item", price=100, quantity=10)

    with pytest.raises(Exception):
        # Should raise an exception
        sample_store.remove_product(fake_product)


def test_get_total_quantity(sample_store):
    """Test getting total quantity of all products in store"""
    # Should be a total of 850
    assert sample_store.get_total_quantity() == (100 + 500 + 250)


def test_get_all_products(sample_store):
    """Test retrieving all active products"""
    active_products = sample_store.get_all_products()

    # All 3 products are active
    assert len(active_products) == 3

    # Deactivate one product
    sample_store.product_list[0].deactivate()
    active_products = sample_store.get_all_products()

    # Should be only 2 products
    assert len(active_products) == 2


def test_order(sample_store):
    """Test ordering products from the store"""
    # Buy 2 MacBooks and 1 Bose Earbuds
    shopping_list = [
        (sample_store.product_list[0], 2),
        (sample_store.product_list[1], 1)
    ]

    total_cost = sample_store.order(shopping_list)

    # Should be a total of 3150
    assert total_cost == (2 * 1450) + (1* 250)
    # Product quantity should be 98 (100 - 2)
    assert sample_store.product_list[0].get_quantity() == 98
    # Product quantity should be 499 (500 - 1)
    assert sample_store.product_list[1].get_quantity() == 499


def test_invalid_order(sample_store):
    """Test ordering out-of-stock product or more than available"""
    out_of_stock_product = Product("Out of Stock Item", price=100, quantity=0, is_active=False)
    sample_store.add_product(out_of_stock_product)
    shopping_list1 = [(out_of_stock_product, 1)]

    shopping_list2 = [(sample_store.product_list[0], 102)]

    # out-of-stock product
    with pytest.raises(Exception):
        sample_store.order(shopping_list1)

    # not enough stock
    with pytest.raises(Exception):
        sample_store.order(shopping_list2)