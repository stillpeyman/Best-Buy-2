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
    # Store should have 3 products
    assert len(sample_store.product_list) == 3


@pytest.mark.parametrize("invalid_products_list", [
    [],
    ("MacBook Air M2", 1450, 100)
])
def test_invalid_init(invalid_products_list):
    with pytest.raises(Exception):
        Store(invalid_products_list)


def test_add_product(sample_store):
    new_product = Product("Sony Alpha 7", price=1700, quantity=10)
    sample_store.add_product(new_product)

    # Product should be added
    assert new_product in sample_store.product_list
    # Store should have 4 products
    assert len(sample_store.product_list) == 4


@pytest.mark.parametrize("invalid_product", [
    "Not a Product object",
    123,
    None,
    [Product("Test", 1, 1)]
])
def test_add_invalid_product(sample_store, invalid_product):
    with pytest.raises(Exception):
        sample_store.add_product(invalid_product)


@pytest.mark.parametrize("fake_product", [
    Product("Nonexistent item", price=100, quantity=10),
    Product("Fake product", price=50, quantity=1)
])
def test_remove_product(sample_store, fake_product):
    with pytest.raises(Exception):
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
    assert sample_store.product_list[0].quantity == 98
    # Product quantity should be 499 (500 - 1)
    assert sample_store.product_list[1].quantity == 499


@pytest.mark.parametrize("shopping_list", [
    [(Product("Out of Stock Item", price=100, quantity=0,
              is_active=False), 1)],
    [(Product("MacBook Air M2", price=1450, quantity=2), 5)]
])
def test_invalid_order(sample_store, shopping_list):
    """
    Test invalid orders (out-of-stock or invalid quantity).
    """
    # Add out-of-stock product to the store if needed
    # unpack tuples in shopping list, only check for product (not quantity!)
    for product, _ in shopping_list:
        if product in sample_store.product_list:
            sample_store.add_product(product)

    with pytest.raises(Exception):
        sample_store.order(shopping_list)


def test_contains(sample_store):
    """
    Test membership of a product in sample_store product list.
    """
    macbook = sample_store.product_list[0]
    earbuds = sample_store.product_list[1]

    assert macbook in sample_store
    assert earbuds in sample_store

    p = Product("Sony Headphones", price=100, quantity=100)
    assert p not in sample_store


def test_add_stores(sample_store):
    """
    Test combining two stores.
    """
    p = Product("Sony Headphones", price=100, quantity=100)
    other_store = Store([p])

    combined_store = sample_store + other_store

    assert isinstance(combined_store, Store)
    assert len(combined_store.product_list) == 4
    assert p in combined_store

    for product in sample_store.product_list:
        assert product in combined_store


@pytest.mark.parametrize("invalid_store", [
    "Not a Store object",
    123,
    None,
    [Store([Product("Test", 1, 1)])]
])
def test_add_invalid_store(sample_store, invalid_store):
    """
    Test combining invalid store with sample_store.
    """
    with pytest.raises(Exception):
        sample_store + invalid_store