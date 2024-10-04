
class Store:
    def __init__(self, products=None):
        if products is None:
            products = []
        self.products = products  # List of product instances

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        return sum(product.get_quantity() for product in self.products)

    def get_all_products(self):
        return [product for product in self.products if product.is_active()]

    def order(self, shopping_list) -> float:
        total_price = 0
        for product, quantity in shopping_list:
            if product in self.products and product.is_active():
                total_price += product.buy(quantity)
            else:
                raise ValueError(f"Product {product.name} is currently unavailable.")
        return total_price

