from products import NonStockedProduct
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


    def order(self, shopping_list):
        total_price = 0.0
        for product, quantity in shopping_list:
            # For NonStockedProduct, you don't need to adjust quantity or check stock
            if isinstance(product, NonStockedProduct):
                total_price += product.price * quantity  # Only the price matters
            else:
                total_price += product.buy(quantity)  # For other products, handle normally
        return total_price

