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
        self.price = float(price)
        self._quantity = quantity
        self._is_active = is_active
        self._promotions = promotions if promotions is not None else []


    @property
    def price(self):
        """
        Getter function for product price.

        Returns:
            float: The price of the product.
        """
        return self._price


    @price.setter
    def price(self, value):
        """
        Setter for product price.

        Args:
            float: The new price of the product.

        Raises:
            Exception: If the price is not a positive number.
        """
        if not isinstance(value, (int, float)) or value <= 0:
            raise Exception("Error, price must be float and greater than 0!")
        self._price = float(value)


    @property
    def quantity(self):
        """
        Getter function for quantity.

        Returns:
             int: Quantity available.
        """
        return self._quantity


    @quantity.setter
    def quantity(self, quantity):
        """
        Setter for quantity.

        Args:
            int: The new quantity of the product.

        Raises:
            Exception: If the quantity is not a valid integer..
        """
        if not isinstance(quantity, int) or quantity < 0:
            raise Exception("Error, quantity must be a positive integer!")

        self._quantity = quantity

        if self._quantity == 0:
            self._is_active = False


    def update_quantity(self, quantity):
        """
        Update the quantity after a purchase.
        Deactivate the product if the quantity reaches zero.

        Args:
            quantity (int): The quantity to reduce from the stock.
        """
        if not isinstance(quantity, int) or quantity < 0:
            raise Exception("Error, quantity must be a positive integer!")

        if quantity > self._quantity:
            raise Exception("Not enough stock to update quantity.")

        self._quantity -= quantity

        if self._quantity == 0:
            self._is_active = False


    @property
    def is_active(self):
        """
        Getter function for active.

        Returns:
             bool: True if the product is active, otherwise False.
        """
        return self._is_active


    @is_active.setter
    def is_active(self, value):
        """
        Setter for product status.
        """
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
        """
        Adds one or more promotions to the product's promotion list.

        If a single promotion is passed, it is added to the list if not already present.
        If a list of promotions is passed, each promotion is checked and added individually
        if not already in the list.

        Args:
            promotion (Promotion or list): A single Promotion object or a list of Promotion objects
        """
        if isinstance(promotion, list):
            for promo in promotion:
                if isinstance(promo, Promotion) and promo not in self._promotions:
                    self._promotions.append(promo)

        elif isinstance(promotion, Promotion):
            if promotion not in self._promotions:
                self._promotions.append(promotion)


    def remove_promo(self, promotion):
        """
        Removes one or more promotions from the product's promotion list.

        If a single promotion is passed, it is removed from the list if it exists.
        If a list of promotions is passed, each promotion is checked and removed individually
        if it exists in the list.

        Args:
            promotion (Promotion or list): A single Promotion object or a list of Promotion objects
        """
        if isinstance(promotion, list):
            for promo in promotion:
                if isinstance(promo, Promotion) and promo in self._promotions:
                    self._promotions.remove(promo)

        elif isinstance(promotion, Promotion):
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


    def promo_text(self):
        """
        Return a formatted string showing applied promos, or empty if none.

        Returns:
             str: Promo description or empty string.
        """
        if self._promotions:
            return f" | PROMOTIONS: {', '.join([str(promo) for promo in self._promotions])}"
        else:
            return ""


    def __str__(self):
        """
        Return a user-friendly string representation of the product.
        """
        if self._promotions:
            promo_text = f" | PROMOTIONS: {', '.join([str(promo) for promo in self._promotions])}"
        else:
            promo_text = ""

        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}{promo_text}"


    def buy(self, quantity):
        """
        Buy a quantity of the product. Applies best available promotion if any.

        Args:
            quantity (int): Quantity to purchase.

        Returns:
            float: Total price after discount.
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

            self.update_quantity(quantity)
            return round(best_price, 2)

        self.update_quantity(quantity)
        return total_price


    def calculate_price(self, quantity):
        """
        Calculate price for a quantity without modifying stock.

        Args:
            quantity (int): Quantity to calculate price for.

        Returns:
            float: Total price with promotions if applicable.
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


    def __lt__(self, other):
        """
        Compare this product to another product for lower-than based on price.

        Args:
            other (Product): The product to compare with.

        Returns:
            bool: True if this product's price is lower than the other's price,
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
        A product type that does not track stock (e.g., digital goods).
        Always has a quantity of 0.
        """
        # Call the constructor of the parent <Product> class
        super().__init__(name, price, 0, is_active)


    def buy(self, quantity):
        """
        Purchase non-stocked product. No inventory restrictions.

        Args:
            quantity (int): Quantity to purchase.

        Returns:
            float: Total price, applying best promotion if available.
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
        if self._promotions:
            promo_text = f" | PROMOTIONS: {', '.join([str(promo) for promo in self._promotions])}"
        else:
            promo_text = ""

        return f"{self.name}, Price: {self.price} (Virtual Product){promo_text}"


class LimitedProduct(Product):
    def __init__(self, name, price, quantity, max_quantity, is_active=True):
        """
        A product with a maximum purchase quantity per order.
        """
        # Call the constructor of the parent <Product> class
        super().__init__(name, price, quantity, is_active)
        self._max_quantity = max_quantity


    @property
    def max_quantity(self):
        """
        int: Maximum quantity allowed per order.
        """
        return self._max_quantity


    def buy(self, quantity):
        """
        Purchase a limited product, enforcing max quantity per order.

        Args:
            quantity (int): Quantity to purchase.

        Returns:
            float: Total price after discount.
        """
        if quantity > self._max_quantity:
            raise Exception(f"Error, you can only buy a maximum of {self._max_quantity} per order!")

        return super().buy(quantity)


    def __str__(self):
        """
        Override <show> to display the order limit on this product.
        """
        return super().__str__() + f" (Max per order: {self._max_quantity})"



