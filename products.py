class Promotion:
    def __init__(self, name: str):
        self.name = name

    def apply_promotion(self, product, quantity) -> float:
        raise NotImplementedError("Subclasses must implement this method.")


class SecondHalfPrice(Promotion):
    def apply_promotion(self, product, quantity) -> float:
        # Assuming this promotion applies to the entire quantity
        return (product.price / 2) * quantity


class ThirdOneFree(Promotion):
    def apply_promotion(self, product, quantity) -> float:
        free_units = quantity // 3  # Get the number of free items
        total_units_to_pay = quantity - free_units
        return product.price * total_units_to_pay


class PercentDiscount(Promotion):
    def __init__(self, name: str, percent: float):
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        return (product.price * (1 - self.percent / 100)) * quantity



class Product:
    def __init__(self, name: str, price: float, quantity: int, is_non_stocked: bool = False):
        """Validate the product name (cannot be empty)"""
        if not name:
            raise ValueError("Product name cannot be empty.")

        if price < 0:
            raise ValueError("Product price cannot be less than zero.")

        if quantity < 0 and not is_non_stocked:
            raise ValueError("Product quantity cannot be negative.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = is_non_stocked or quantity > 0  # Always active if non-stocked
        self.promotion = None  # Initialize promotion to None

    def get_quantity(self) -> int:
        """gets quantity"""
        return self.quantity

    def set_quantity(self, quantity: int):
        """sets the quantity"""
        self.quantity = quantity
        self._update_active_status()  # Call the helper method to check if it needs to be deactivated

    def is_active(self) -> bool:
        """checks that its active"""
        return self.active

    def activate(self):
        """activates products"""
        self.active = True

    def deactivate(self):
        """deactivates products"""
        self.active = False

    def _update_active_status(self):
        """method to deactivate if quantity is 0"""
        if self.quantity == 0:
            self.deactivate()
        else:
            self.activate()

    def show(self) -> str:
        promotion_info = f", Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: {self.price:.2f}{promotion_info}, Quantity: {self.quantity}"

    def buy(self, quantity: int) -> float:
        """Calculate the total price after applying any promotions."""
        if self.quantity < quantity:
            raise ValueError(f"Not enough quantity available. Only {self.quantity} left in stock.")
        # Calculate price based on promotion if it exists
        if self.promotion:
            discounted_price = self.promotion.apply_promotion(self, quantity)
            self.quantity -= quantity
            self._update_active_status()
            return discounted_price

        self.quantity -= quantity
        self._update_active_status()  # Reuse the helper method to check for deactivation
        return self.price * quantity


class NonStockedProduct(Product):
    """Non-Stocked Product class"""
    def __init__(self, name: str, price: float):
        super().__init__(name, price, quantity=0, is_non_stocked=True)  # Set quantity to 0 and mark as non-stocked

    def show(self) -> str:
        return f"{self.name} (Non-Stocked), Price: {self.price}, Quantity: not specified"


class LimitedProduct(Product):
    """Limited Quantity Product class"""
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def buy(self, quantity: int) -> float:
        """Check if the quantity exceeds the maximum allowed per order"""
        if quantity > self.maximum:
            raise ValueError(f"Cannot purchase more than {self.maximum} of {self.name}.")
        return super().buy(quantity)

    def show(self) -> str:
        """Indicate the maximum purchase limit"""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Maximum: {self.maximum}"
