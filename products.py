class Product:

    def __init__(self, name, price, quantity, is_active=True):
        """
        Gets product name, price and quantity and initializes
        a product, by default is_active (availability) set to 'True'.
        """
        if not isinstance(name, str) or not name:
            raise Exception("Error, name must be a non-empty string!")

        if not isinstance(price, (int, float)) or price <= 0:
            raise Exception("Error, price must be float and greater than 0!")

        if not isinstance(quantity, int) or quantity < 0:
            raise Exception("Error, quantity must be a positive integer!")

        self.name = name
        self.price = float(price)
        self.quantity = quantity
        self.is_active = is_active


    def get_quantity(self):
        """
        Getter function for quantity.
        Returns the quantity (int).
        """
        return self.quantity


    def set_quantity(self, quantity):
        """
        Setter function for quantity.
        If quantity reaches 0, deactivates the product.
        """
        if not isinstance(quantity, int) or quantity < 0:
            raise Exception("Error, quantity must be a positive integer!")

        self.quantity += quantity

        if self.quantity == 0:
            self.is_active = False


    def get_status(self):
        """
        Getter function for active. Returns True
        if the product is active, otherwise False.
        """
        return self.is_active


    def activate(self):
        """
        Activates the product.
        """
        self.is_active = True


    def deactivate(self):
        """
        Deactivates the product.
        """
        self.is_active = False


    def show(self):
        """
        Returns a string that represents the product.
        """
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"


    def buy(self, quantity):
        """
        Buys a given quantity of the product.
        Returns total price (float) of the purchase.
        Updates the quantity of the product.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise Exception("Error, quantity must be integer and greater than 0!")

        if quantity > self.quantity:
            raise Exception("Error, insufficient quantity!")

        if not self.is_active:
            raise Exception("Error, product is out of stock!")

        self.quantity -= quantity

        if self.quantity == 0:
            self.is_active = False

        return self.price * quantity


class NonStockedProduct(Product):
    def __init__(self, name, price, is_active=True):
        """
        Gets product name, price, quantity and initializes
        a product.

        Status by default is_active (availability) set to 'True'.

        Quantity always set to 0 because a non-stocked product is not physical.
        """
        # Call the constructor of the parent <Product> class
        super().__init__(name, price, 0, is_active)


    def show(self):
        """
        Override <show> to display that it is a non-stocked product.
        """
        return f"{self.name}, Price: {self.price}, This is a non-stocked product!"


    def buy(self, quantity):
        """
        Buys a given quantity of the non-stocked product.
        Since the product doesn't track quantity, it will always return the price * quantity
        as long as the product is active. Quantity (stock) is not limited or decreased.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise Exception("Error, quantity must be integer and greater than 0!")

        if not self.is_active:
            raise Exception("Error, product is unavailable at the moment!")

        return self.price * quantity


class LimitedProduct(Product):
    def __init__(self, name, price, quantity, max_quantity, is_active=True):
        """
        Gets product name, price, quantity, max quantity per order and initializes
        a product, by default is_active (availability) set to 'True'.
        """
        # Call the constructor of the parent <Product> class
        super().__init__(name, price, quantity, is_active)
        self.max_quantity = max_quantity


    def buy(self, quantity):
        """
        Override <buy> to restrict the quantity that can be purchased.
        """
        if quantity > self.max_quantity:
            raise Exception(f"Error, you can only buy a maximum of {self.max_quantity} per order!")

        return super().buy(quantity)


    def show(self):
        """
        Override <show> to display the order limit on this product.
        """
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Max per order: {self.max_quantity}"