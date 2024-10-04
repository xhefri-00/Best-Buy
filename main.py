from products import Product
from store import Store

def create_default_inventory():
    """Initial stock of inventory"""
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250)
    ]
    best_buy = Store(product_list)
    return best_buy


def start(store):
    """Store Menu Displqy"""
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

            while True:
                print("\nAvailable Products:")
                for idx, product in enumerate(products, 1):
                    print(f"{idx}. {product.show()}")

                product_choice = input("\nEnter the number of the product you would like to order (Enter empty text to finish): ")

                """If user enters empty input, finish the order process"""
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

                while True:
                    try:
                        quantity = int(input(f"What amount would you like for {product.name}? "))

                        if quantity == 0:
                            print("Okay, order was not placed.")
                            break

                        if quantity > product.get_quantity():
                            print(f"Unfortunately, we currently have {product.get_quantity()} in stock.")
                            reconsider = input("Would you like to reconsider the amount? (yes or no): ").strip().lower()
                            if reconsider != 'yes':
                                break
                        else:
                            shopping_list.append((product, quantity))
                            print(f"Product {product.name} added to list!")
                            break
                    except ValueError:
                        print("Please enter a valid number for quantity.")

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
