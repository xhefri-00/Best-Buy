class Product:
    def __init__(self, name: str, price: float, quantity: int):
        """Validate the product name (cannot be empty)"""
        if not name:
            raise ValueError("Product name cannot be empty.")

        if price < 0:
            raise ValueError("Product price cannot be less then zero.")

        if quantity < 0:
            raise ValueError("Product quantity cannot be less than zero.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = quantity > 0  # The product is active if quantity is greater than 0


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
        """Including the active status in the display"""
        active_status = "Active" if self.active else "Inactive"
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity} ({active_status})"


    def buy(self, quantity: int) -> float:
        """Error handling for available quantity"""
        if self.quantity < quantity:
            raise ValueError(f"Not enough quantity available. Only {self.quantity} left in stock.")

        self.quantity -= quantity
        self._update_active_status()  # Reuse the helper method to check for deactivation

        return self.price * quantity
