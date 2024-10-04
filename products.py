class Product:
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = quantity > 0  # The product is active if the quantity is greater than 0

    def get_quantity(self) -> float:
        return self.quantity

    def set_quantity(self, quantity: int):
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()  # Deactivate the product if the quantity is zero

    def is_active(self) -> bool:
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity: int) -> float:
        if self.quantity < quantity:
            raise ValueError("Not enough quantity available")
        self.quantity -= quantity
        if self.quantity == 0:
            self.deactivate()  # Deactivate if quantity becomes zero
        return self.price * quantity
