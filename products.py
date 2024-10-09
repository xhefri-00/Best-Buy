class Product:
    def __init__(self, name: str, price: float, quantity: int, is_non_stocked: bool = False):
        """Validate the product name (cannot be empty)"""
        if not name:
            raise ValueError("Product name cannot be empty.")

        if price < 0:
            raise ValueError("Product price cannot be less then zero.")

        if quantity < 0 and not is_non_stocked:
            raise ValueError("Product quantity cannot be negative.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = is_non_stocked or quantity > 0  # Always active if non-stocked


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
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"


    def buy(self, quantity: int) -> float:
        """Error handling for available quantity"""
        if self.quantity < quantity:
            raise ValueError(f"Not enough quantity available. Only {self.quantity} left in stock.")

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
        return f"{self.name} (Limited to {self.maximum} per order), Price: {self.price}, Quantity: {self.quantity}"