from products import Product


class Store:

    def __init__(self, product_list):
        """
        Initialize the store with a list of products.

        Args:
            product_list (list): A non-empty list of Product instances.

        Raises:
            Exception: If the product_list is not a list or is empty.
        """
        if not isinstance(product_list, list) or not product_list:
            raise Exception("product_list must be a non-empty list!")
        self.product_list = product_list

    def add_product(self, product: Product):
        """
        Add a product to the store.

        Args:
            product (Product): The product to be added.
        """
        if not isinstance(product, Product):
            raise Exception("Only instances of Product can be added!")
        self.product_list.append(product)

    def remove_product(self, product: Product):
        """
        Remove a product from the store.

        Args:
            product (Product): The product to be removed.
        """
        if product in self.product_list:
            self.product_list.remove(product)
        else:
            raise Exception("Product not found in store!")

    def get_total_quantity(self):
        """
        Get the total quantity of all products in the store.

        Returns:
            int: The total number of items across all products.
        """
        return sum(product.quantity for product in self.product_list)

    def get_all_products(self):
        """
        Get a list of all active products as strings.

        Returns:
            list of str: A list of string representations of active products.
        """
        return [str(product) for product in self.product_list if product.is_active]

    def get_active_products(self):
        """
        Get a list of all active product objects in the store.

        Returns:
            list of Product: All active Product instances.
        """
        return [product for product in self.product_list if product.is_active]

    def order(self, shopping_list):
        """
        Process an order and return the total price.

        Args:
            shopping_list (list of tuples): Each tuple contains a Product instance
                                            and a quantity to purchase (int).

        Returns:
            float: The total price of the order.

        Raises:
            Exception: If the product cannot be bought (e.g., not enough stock).
        """
        total_price = 0.0
        for product, quantity in shopping_list:
            total_price += product.buy(quantity)
        return total_price

    def calculate_subtotal(self, shopping_list):
        """
        Calculate the sub-total of a current order.

        Args:
            shopping_list (list): List of tuples (product: Product, quantity: int).

        Returns:
            float: Sub-total of a current order.
        """
        sub_total = 0.0
        for product, quantity in shopping_list:
            sub_total += product.calculate_price(quantity)
        return sub_total

    def __contains__(self, product):
        """
        Check if a product is in the store.

        Args:
            product (Product): The product to check.

        Returns:
            bool: True if the product is in the store, False otherwise.
        """
        if not isinstance(product, Product):
            raise False

        return product in self.product_list

    def __add__(self, other):
        """
        Combine two Store instances into a new Store containing all products from both.

        Args:
            other (Store): Another Store instance to be combined.

        Returns:
            Store: A new Store instance containing all products from both stores.
        """
        if not isinstance(other, Store):
            raise Exception(f"{other} must be Store instance.")
        combined_products = self.product_list + other.product_list
        return Store(combined_products)

