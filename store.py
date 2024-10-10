from products import NonStockedProduct

class Store:
    """Class representing a store that manages products and orders."""
    def __init__(self, products=None):
        """Initialize the store with a list of products."""
        if products is None:
            products = []
        self.products = products  # List of product instances


    def add_product(self, product):
        """Add a product to the store's product list."""
        self.products.append(product)


    def remove_product(self, product):
        """Remove a product from the store's product list."""
        self.products.remove(product)


    def get_total_quantity(self) -> int:
        """Get the total quantity of all products in the store."""
        return sum(product.get_quantity() for product in self.products)


    def get_all_products(self):
        """Retrieve all active products in the store."""
        return [product for product in self.products if product.is_active()]


    def order(self, shopping_list):
        """Place an order based on the shopping list and calculate the total price."""
        total_price = 0.0
        added_products = {}  # Track quantities for NonStockedProducts

        for product, quantity in shopping_list:
            # Check if product is non-stocked
            if isinstance(product, NonStockedProduct):
                # Non-stocked products do not deplete in quantity
                if product in added_products:
                    print(
                        f"You already have {added_products[product]} of {product.name} in the cart. Quantity is not limited for non-stocked products.")
                else:
                    total_price += product.price * quantity  # Only price matters for non-stocked products
                    added_products[product] = quantity  # Tracks the quantity in the cart
            else:
                # Regular products with stock limits
                remaining_quantity = product.get_quantity()
                if remaining_quantity < quantity:
                    print(
                        f"The order for {product.name} cannot exceed inventory. There are only {remaining_quantity} left.")
                    continue  # Skip this product if not enough stock

                # If promotion exists, apply it and call `buy` to reduce stock
                if product.promotion:
                    discounted_price = product.promotion.apply_promotion(product, quantity)
                    print(
                        f"Applied Promotion on {product.name}. Discounted total for {quantity} is: {discounted_price:.2f} $.")
                    total_price += discounted_price
                else:
                    total_price += product.buy(quantity)  # Reduce stock and calculate regular price
        return total_price
