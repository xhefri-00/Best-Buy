class Promotion:
    """Base class for promotions."""
    def __init__(self, name: str):
        """Initialize promotion with name."""
        self.name = name


    def apply_promotion(self, product, quantity) -> float:
        """Apply promotion logic to product and quantity."""
        raise NotImplementedError("Subclasses must implement this method.")


class SecondHalfPrice(Promotion):
    """Promotion: buy two, get the second one half-price."""
    def apply_promotion(self, product, quantity) -> float:
        """Apply the second half-price promotion."""
        if quantity == 1:
            return product.price
        elif quantity % 2 == 0:
            # If even number, half of them are full price, half are half price
            return (quantity // 2) * product.price + (quantity // 2) * (product.price / 2)
        else:
            # If odd number, apply half price to (quantity-1) and full price to 1 unit
            return ((quantity // 2) * product.price + (quantity // 2) * (product.price / 2)) + product.price


class ThirdOneFree(Promotion):
    """Promotion: buy two, get the third one free."""
    def apply_promotion(self, product, quantity) -> float:
        """Apply the third-one-free promotion."""
        free_units = quantity // 3  # Get the number of free items
        total_units_to_pay = quantity - free_units
        return product.price * total_units_to_pay


class PercentDiscount(Promotion):
    """Promotion: percentage discount."""
    def __init__(self, name: str, percent: float):
        """Initialize percentage discount promotion."""
        super().__init__(name)
        self.percent = percent


    def apply_promotion(self, product, quantity) -> float:
        """Apply the percent discount."""
        return (product.price * (1 - self.percent / 100)) * quantity


class Product:
    """Represents a product with a price and quantity."""
    def __init__(self, name: str, price: float, quantity: int, is_non_stocked: bool = False):
        """Initialize the product."""
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
        self.promotion = None  # Initializes promotion to None


    def get_quantity(self) -> int:
        """Return the quantity of the product."""
        return self.quantity


    def set_quantity(self, quantity: int):
        """Set the quantity and update the product's active status."""
        self.quantity = quantity
        self._update_active_status()


    def set_promotion(self, promotion):
        """Set the promotion for the product."""
        self.promotion = promotion


    def is_active(self) -> bool:
        """Return whether the product is active."""
        return self.active


    def activate(self):
        """Activate the product."""
        self.active = True


    def deactivate(self):
        """Deactivate the product if out of stock."""
        self.active = False


    def _update_active_status(self):
        """Update the product's active status based on quantity."""
        if self.quantity == 0:
            self.deactivate()
        else:
            self.activate()


    def show(self):
        """Show product details including the current promotion."""
        quantity_display = f"Quantity: {self.get_quantity()}" if not isinstance(self, NonStockedProduct) else "Quantity: not specified"
        promo_display = f", Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: {self.price:.2f}{promo_display}, {quantity_display}"


    def buy(self, quantity: int) -> float:
        """Calculate the total price after applying any promotions."""
        if self.quantity < quantity:
            raise ValueError(f"Not enough quantity available. Only {self.quantity} left in stock.")

        # Calculate price based on promotion if it exists
        if self.promotion:
            discounted_price = self.promotion.apply_promotion(self, quantity)
        else:
            discounted_price = self.price * quantity

        self.quantity -= quantity
        self._update_active_status()

        return discounted_price


class NonStockedProduct(Product):
    """Non-stocked product class."""
    def __init__(self, name: str, price: float):
        """Initialize a non-stocked product."""
        super().__init__(name, price, quantity=0, is_non_stocked=True)


    def buy(self, quantity):
        """Override buy method for NonStockedProduct to skip stock check."""
        # Apply promotion if there is one
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        else:
            return self.price * quantity  # No promotion, return regular price


    def show(self) -> str:
        """Show non-stocked product with promotion if available."""
        promo_display = f", Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name} (Non-Stocked), Price: {self.price}{promo_display}, Quantity: not specified"


class LimitedProduct(Product):
    """Limited quantity product class."""
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        """Initialize a limited quantity product."""
        super().__init__(name, price, quantity)
        self.maximum = maximum


    def buy(self, quantity: int) -> float:
        """Check if the quantity exceeds the maximum allowed per order."""
        if quantity > self.maximum:
            raise ValueError(f"Cannot purchase more than {self.maximum} of {self.name}.")
        return super().buy(quantity)


    def show(self) -> str:
        """Indicate the maximum purchase limit."""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Maximum: {self.maximum}"