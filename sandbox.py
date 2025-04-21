from promotions import Promotion


class Product:

    def __init__(self, name, price, quantity, is_active=True, promotions=None):
        """
        A class representing a product.

        Attributes:
            name (str): The name of the product.
            price (float): The price per unit.
            quantity (int): The available quantity in stock.
            is_active (bool): Whether the product is active/available for purchase.
            promotions (list): List of promotion instances applied to this product.
        """
        if not isinstance(name, str) or not name:
            raise Exception("Error, name must be a non-empty string!")

        if not isinstance(price, (int, float)) or price <= 0:
            raise Exception("Error, price must be float and greater than 0!")

        if not isinstance(quantity, int) or quantity < 0:
            raise Exception("Error, quantity must be a positive integer!")

        if promotions:
            for promotion in promotions:
                if not isinstance(promotion, Promotion):
                    raise Exception("Only instance of Promotion can be used.")

        self.name = name
        self._price = float(price)
        self._quantity = quantity
        self._is_active = is_active
        self._promotions = promotions if promotions is not None else []


    @property
    def price(self):
        return self._price


    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise Exception("Error, price must be float and greater than 0!")
        self._price = float(value)


    @property
    def quantity(self):
        """
        Getter function for quantity.
        Return the quantity (int).
        """
        return self._quantity


    @quantity.setter
    def quantity(self, quantity):
        """
        Setter function for quantity.
        If quantity reaches 0, deactivate the product.
        """
        if not isinstance(quantity, int) or quantity < 0:
            raise Exception("Error, quantity must be a positive integer!")

        self._quantity = quantity

        if self._quantity == 0:
            self._is_active = False


    @property
    def is_active(self):
        """
        Getter function for active. Return True
        if the product is active, otherwise False.
        """
        return self._is_active


    @is_active.setter
    def is_active(self, value):
        self._is_active = bool(value)


    def activate(self):
        """
        Activate the product.
        """
        self._is_active = True


    def deactivate(self):
        """
        Deactivate the product.
        """
        self._is_active = False


    def add_promo(self, promotion):
        if isinstance(promotion, Promotion):
            if promotion not in self._promotions:
                self._promotions.append(promotion)


    def remove_promo(self, promotion):
        if isinstance(promotion, Promotion):
            if promotion in self._promotions:
                self._promotions.remove(promotion)


    @property
    def promo(self):
        """
        Getter for promo.
        """
        return self._promotions


    @promo.setter
    def promo(self, promotions):
        """
        Setter for promo.
        """
        if not isinstance(promotions, list):
            # If a single promo is passed, make it a list
            promotions = [promotions]

        self._promotions = promotions


    def __str__(self):
        """
        Return a string that represents the product.
        """
        if self._promotions:
            promo_text = f" | Promotions: {', '.join([str(promo) for promo in self._promotions])}"
        else:
            promo_text = ""

        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}{promo_text}"


    def buy(self, quantity):
        """
        Buy a given quantity of the product.
        Return total price (float) of the purchase.
        Update the quantity of the product.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise Exception("Error, quantity must be integer and greater than 0!")

        if quantity > self._quantity:
            raise Exception("Error, insufficient quantity!")

        if not self._is_active:
            raise Exception("Error, product is out of stock!")

        total_price = self.price * quantity

        # Apply promo(s) if available, get <best_price> if multiple promos
        if self._promotions:
            best_price = min(
                [promo.apply_promotion(self, quantity) for promo in self._promotions],
                default=total_price
            )
            return round(best_price, 2)

        self._quantity -= quantity
        if self._quantity == 0:
            self._is_active = False

        return total_price


    def __lt__(self, other):
        """
        Compare this product to another product for greater-than based on price.

        Args:
            other (Product): The product to compare with.

        Returns:
            bool: True if this product's price is greater than the other's price,
            False otherwise.
        """
        if not isinstance(other, Product):
            raise Exception(f"{other} must be a Product instance!")
        return self.price < other.price


    def __gt__(self, other):
        """
        Compare this product to another product for greater-than based on price.

        Args:
            other (Product): The product to compare with.

        Returns:
            bool: True if this product's price is greater than the other's price,
            False otherwise.
        """
        if not isinstance(other, Product):
            raise Exception(f"{other} must be a Product instance!")
        return self.price > other.price


class NonStockedProduct(Product):
    def __init__(self, name, price, is_active=True):
        """
        Get product name, price, quantity and initializes
        a product.

        Status by default is_active (availability) set to 'True'.

        Quantity always set to 0 because a non-stocked product is not physical.
        """
        # Call the constructor of the parent <Product> class
        super().__init__(name, price, 0, is_active)


    def buy(self, quantity):
        """
        Buy a given quantity of the non-stocked product.
        Since the product doesn't track quantity, it will always return the price * quantity
        as long as the product is active. Quantity (stock) is not limited or decreased.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise Exception("Error, quantity must be integer and greater than 0!")

        if not self._is_active:
            raise Exception("Error, product is unavailable at the moment!")

        total_price = self.price * quantity

        # Apply promo(s) if available, get <best_price> if multiple promos
        if self._promotions:
            best_price = min(
                [promo.apply_promotion(self, quantity) for promo in self._promotions],
                default=total_price
            )
            return round(best_price, 2)

        return total_price


    def __str__(self):
        """
        Override <show> to display that it is a non-stocked product.
        """
        return super().__str__() + " (This is a non-stocked product!)"


class LimitedProduct(Product):
    def __init__(self, name, price, quantity, max_quantity, is_active=True):
        """
        Get product name, price, quantity, max quantity per order and initializes
        a product, by default is_active (availability) set to 'True'.
        """
        # Call the constructor of the parent <Product> class
        super().__init__(name, price, quantity, is_active)
        self._max_quantity = max_quantity


    @property
    def max_quantity(self):
        return self._max_quantity


    def buy(self, quantity):
        """
        Override <buy> to restrict the quantity that can be purchased.
        """
        if quantity > self._max_quantity:
            raise Exception(f"Error, you can only buy a maximum of {self._max_quantity} per order!")

        return super().buy(quantity)


    def __str__(self):
        """
        Override <show> to display the order limit on this product.
        """
        return super().__str__() + f" (Max per order: {self._max_quantity})"


class Store:

    def __init__(self, product_list):
        """
        Get a list of products and initializes the store.
        """
        if not isinstance(product_list, list) or not product_list:
            raise Exception("product_list must be a non-empty list!")
        self.product_list = product_list


    def add_product(self, product: Product):
        """
        Add a product to the store provided product is class Product.
        """
        if not isinstance(product, Product):
            raise Exception("Only instances of Product can be added!")
        self.product_list.append(product)


    def remove_product(self, product: Product):
        """
        Remove a product (Product class) from store.
        """
        if product in self.product_list:
            self.product_list.remove(product)
        else:
            raise Exception("Product not found in store!")


    def get_total_quantity(self):
        """
        Return how many items are in the store in total.
        """
        return sum(product.quantity for product in self.product_list)


    def get_all_products(self):
        """
        Return a list of all products in the store that are active.
        """
        return [str(product) for product in self.product_list if product.is_active]


    def order(self, shopping_list):
        """
        Get a list of tuples, each tuple has 2 items (product: Product, quantity),
        buys the product and returns total price of the order.
        """
        total_price = 0.0
        for product, quantity in shopping_list:
            total_price += product.buy(quantity)
        return total_price


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
        if not isinstance(other, Store):
            raise Exception(f"{other} must be Store instance.")
        combined_products = self.product_list + other.product_list
        return Store(combined_products)


# setup initial stock of inventory
mac =  Product("MacBook Air M2", price=1450, quantity=100)
bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
pixel = LimitedProduct("Google Pixel 7", price=500, quantity=250, max_quantity=1)

best_buy = Store([mac, bose])

try:
    mac.price = -100         # Should give error
except Exception as e:
    print(e)

print(mac)               # Should print `MacBook Air M2, Price: $1450 Quantity:100`
print(mac > bose)        # Should print True
print(mac in best_buy)   # Should print True
print(pixel in best_buy) # Should print False

