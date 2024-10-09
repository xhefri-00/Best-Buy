from products import Product, NonStockedProduct, LimitedProduct
from store import Store

def create_default_inventory():
    """Initial stock of inventory"""
    product_list = [Product("MacBook Air M2", price=1450, quantity=100),
                    Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    Product("Google Pixel 7", price=500, quantity=250),
                    NonStockedProduct("Windows License", price=125),
                    LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                    ]
    best_buy = Store(product_list)
    return best_buy


def start(store):
    """Store Menu Display"""
    while True:
        print("**********\nStore Menu:\n__________")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit\n__________")

        choice = input("Please enter your choice: ")

        if choice == '1':
            print("\nAvailable Products:")
            products = store.get_all_products()
            for product in products:
                print(product.show())

        elif choice == '2':
            total_quantity = store.get_total_quantity()
            print(f"\nTotal amount of products in store: {total_quantity}")

        elif choice == '3':
            print("\nMaking an order:")
            products = store.get_all_products()
            if not products:
                print("No products available for order.")
                continue

            shopping_list = []
            shipping_added = False  #Before any products are added, shipping hasn't been selected.

            while True:
                print("\nAvailable Products:")
                for idx, product in enumerate(products, 1):
                    print(f"{idx}. {product.show()}")
                product_choice = input("\nEnter the number of the product you would like to order (Enter empty text to finish): ")
                # If user enters empty input, finish the order process
                if not product_choice:
                    break

                try:
                    product_choice = int(product_choice)
                    if 1 <= product_choice <= len(products):
                        product = products[product_choice - 1]

                    else:
                        print("Invalid product number. Please select a valid option.")
                        continue

                except ValueError:
                    print("Invalid input. Please enter a valid product number.")
                    continue

                if not product.is_active():
                    print(f"Sorry, {product.name} is currently unavailable.")
                    continue

                if isinstance(product, LimitedProduct):
                    # Prevent the user from adding the shipping product again
                    if shipping_added:
                        print("Shipping has already been added to your order.")
                        continue
                    # Automatically add LimitedProduct (like Shipping) with a quantity of 1

                    shopping_list.append((product, 1))  # Add it as 1 since it's limited
                    shipping_added = True  # Setting shipping to True to prevent adding again

                    print(f"Product {product.name} added to list!")
                    continue  # continue product selection

                elif isinstance(product, NonStockedProduct):
                    # Handle NonStockedProduct and allow user to specify the quantity
                    while True:
                        try:
                            quantity = int(input(f"What amount would you like for {product.name}? "))
                            if quantity < 0:
                                raise ValueError("The amount cannot be a negative number.")
                            shopping_list.append((product, quantity))  # Add specified quantity
                            print(f"Product {product.name} added to list!")
                            break

                        except ValueError as e:
                            print(e)  # Print the error message

                else:
                    # For regular stocked products
                    while True:
                        try:
                            quantity = int(input(f"What amount would you like for {product.name}? "))
                            if quantity < 0:
                                raise ValueError("The amount cannot be a negative number.")
                            if quantity == 0:
                                print("Okay, order was not placed.")
                                break

                            if quantity > product.get_quantity():
                                print(f"Unfortunately, we currently have {product.get_quantity()} in stock.")
                                reconsider = input(
                                    "Would you like to reconsider the amount? (yes or no): ").strip().lower()
                                if reconsider != 'yes':
                                    break

                            else:
                                shopping_list.append((product, quantity))
                                print(f"Product {product.name} added to list!")
                                break

                        except ValueError as e:
                            print(e)  # Print the error message

            if shopping_list:
                total_price = store.order(shopping_list)
                print(f"\nTotal price for the order: {total_price} dollars")

        elif choice == '4':
            print("Best Buy says Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")


def main():
    """Creates the inventory and store"""
    best_buy = create_default_inventory()
    start(best_buy)


if __name__ == "__main__":
    main()
