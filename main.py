import textwrap
import products
import store
from products import NonStockedProduct, LimitedProduct


def exit_store():
    """Exits the program"""
    print("Goodbye!")


def make_order(store_instance):
    """Handles making an order"""
    list_all_products(store_instance)
    print("When you want to finish order, enter empty text.")

    shopping_list = []

    while True:
        user_order = input("Enter the product # you want: ").strip()

        if user_order == "":
            break

        if not user_order.strip():
            print("Empty input not valid. Please enter a product #.")
            continue

        try:
            product_index = int(user_order) - 1
            store_inventory = store_instance.product_list
            if product_index < 0 or product_index >= len(store_inventory):
                print("Invalid product number. Try again.")
                continue

            product = store_inventory[product_index]

            while True:
                quantity_to_buy = input("Enter the quantity you want: ").strip()

                if user_order == "":
                    break

                if not quantity_to_buy.isdigit():
                    print("Please enter a valid number for the quantity.")
                    continue

                quantity_to_buy = int(quantity_to_buy)

                if isinstance(product, NonStockedProduct):
                    break

                if isinstance(product, LimitedProduct):
                    if quantity_to_buy > product.max_quantity:
                        print(f"The maximum quantity you can buy is {product.max_quantity}.")
                        continue
                    else:
                        break

                if quantity_to_buy <= 0 or quantity_to_buy > product.quantity:
                    print(f"Please enter an quantity between 1 and {product.quantity}.")
                    continue

                else:
                    break

            shopping_list.append((product, quantity_to_buy))
            print(f"Your current total is {store_instance.order(shopping_list)}")
            list_all_products(store_instance)

        except ValueError:
            print("Invalid input. Please enter a number.")

    if shopping_list:
        print("*" * 10)
        print(f"Order made! Total payment {store_instance.order(shopping_list)}")


def show_total_quantity(store_instance):
    """Shows the total number of items in the store"""
    print(f"\nTotal of {store_instance.get_total_quantity()} items in store.")


def list_all_products(store_instance):
    """Lists of all products in the store"""
    print("-" * 10)
    for index, product in enumerate(store_instance.get_all_products(), start=1):
        print(f"{index}. {product}")
    print("-" * 10)


def execute_user_choice(store_instance):
    """Handles user input and calls corresponding function"""
    choices = {
        "1": list_all_products,
        "2": show_total_quantity,
        "3": make_order,
        "4": exit_store
    }

    while True:
        user_choice = input("\nPlease choose a number: ").strip()
        action = choices.get(user_choice)

        if user_choice == "4":
            exit_store()
            break

        elif action:
            action(store_instance)
        else:
            print("Invalid choice, please try again.")

        start()


def start():
    """Displays the store menu"""
    width = 30
    menu = textwrap.dedent(f"""
        {"Store Menu".center(width)}
        {"-" * 29}
        1. List all products in store
        2. Show total amount in store
        3. Make an order
        4. Quit""")
    print(menu)


def main():
    """Main function starts the program"""
    # setup initial stock of inventory
    product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                    products.Product("Google Pixel 7", price=500, quantity=250),
                    products.NonStockedProduct("Windows License", price=125),
                    products.LimitedProduct("Shipping", price=10, quantity=250, max_quantity=1)
                    ]

    # create Store instance
    best_buy = store.Store(product_list)
    start()
    execute_user_choice(best_buy)


if __name__ == "__main__":
    main()

