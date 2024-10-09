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
        added_products = {}  # Track quantities for NonStockedProducts

        for product, quantity in shopping_list:
            # Apply promotion if it exists
            if product.promotion:
                discounted_price = product.promotion.apply_promotion(product, quantity)
                total_price += discounted_price
                print(f"Applied 30% OFF promotion on {product.name}. Discounted total for {quantity} is: {discounted_price:.2f} $.")
            else:
                if isinstance(product, NonStockedProduct):
                    if product in added_products:
                        print(
                            f"You already have {added_products[product]} of {product.name} in the cart. Quantity is not limited for non-stocked products.")
                    else:
                        total_price += product.price * quantity  # Only the price matters
                        added_products[product] = quantity  # Track the quantity in the cart
                else:
                    # Check stock for regular products
                    remaining_quantity = product.get_quantity()
                    if remaining_quantity < quantity:
                        print(
                            f"The order for {product.name} cannot exceed inventory. There are only {remaining_quantity} left.")
                        continue  # Skip this product if not enough stock
                    total_price += product.buy(quantity)  # For other products, handle normally

        return total_price








