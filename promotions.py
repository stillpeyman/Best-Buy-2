from abc import ABC, abstractmethod


class Promotion(ABC):
    """
    Abstract base class for promotions.

    Subclasses must implement the apply_promotion method to calculate
    the final price of a product after applying the promotion.
    """
    def __init__(self, name):
        """
        Initialize the promotion with a name.

        Args:
            name (str): The name of the promotion.
        """
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """
        Calculate the price after applying the promotion.

        Args:
            product: The product object to which the promotion is applied.
            quantity (int): Number of items purchased.

        Returns:
            float: Total price after applying the promotion.
        """
        pass

    def __str__(self):
        """
        Return the name of the promotion.

        Returns:
            str: Name of the promotion.
        """
        return f"{self.name}"


class PercentDiscount(Promotion):
    """
    Promotion that applies a percentage discount on the total price.
    """
    def __init__(self, name, percent):
        """
        Initialize the percentage discount promotion.

        Args:
            name (str): Name of the promotion.
            percent (float): Discount percentage (e.g., 20 for 20% off).
        """
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        """
        Apply percentage discount to the total price.

        Returns:
            float: Discounted total price.
        """
        return product.price * quantity * (1 - self.percent / 100)


class SecondHalfPrice(Promotion):
    """
    Promotion where the second item in each pair is half price.
    """
    def apply_promotion(self, product, quantity) -> float:
        """
        Apply 'second item half price' logic to the total price.

        Returns:
            float: Total price after applying the promotion.
        """
        pairs = quantity // 2
        remainder = quantity % 2
        return (pairs * 1.5 * product.price) + (remainder * product.price)


class ThirdOneFree(Promotion):
    """
    Promotion where every third item is free.
    """
    def apply_promotion(self, product, quantity) -> float:
        """
        For every three items, the third one is free.

        Returns:
            float: Total price after applying the promotion.
        """
        # get groups of 3 (each pay price * 2) and get remainder
        paid_quantity = (quantity // 3) * 2 + (quantity % 3)
        return paid_quantity * product.price

