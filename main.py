import products
import promotions
import store


def display_menu():
    """
    Display the store menu.
    """
    title = "STORE MENU"
    options = [
        "1. List all products in store",
        "2. Show total amount in store",
        "3. Make an order",
        "4. Quit"
    ]

    # space on each side
    padding = 4

    # centered title, underlined with dashes
    lines = [title.center(40)]

    # determine max width
    max_length = max(len(line) for line in lines)
    width = max_length + padding * 2
    border = "*" * (width + 2)

    # dashed lines under title but in full width
    dash_line = "–" * (width - 2)
    lines.append(dash_line)

    # left-aligned options
    for option in options:
        lines.append(option)

    # print framed border
    print(border)
    # top spacing
    print("*" + " " * width + "*")

    for i, line in enumerate(lines):
        # center first two lines
        if i < 2:
            padded_line = line.center(width)

        else:
            # left-align options
            padded_line = (" " * 4 + line).ljust(width)

        print(f"*{padded_line}*")

    # bottom spacing
    print("*" + " " * width + "*")
    print(border)


def start(store_instance):
    """
    Handle user input and calls corresponding function.
    """
    display_menu()

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
            input("\nPress ENTER to get back to the MENU.")
            print()
            display_menu()

        else:
            print("Invalid choice, please try again.")


def list_all_products(store_instance):
    """
    List of all products in the store.
    """
    if len(store_instance.get_all_products()) == 0:
        print_framed_message("EVERYTHING IS SOLD OUT!")

    else:
        print("-" * 10)
        for index, product in enumerate(store_instance.get_all_products(), start=1):
            print(f"{index}. {product}")
        print("-" * 10)


def show_total_quantity(store_instance):
    """
    Show the total number of items in the store.
    """
    print(f"\nTotal of {store_instance.get_total_quantity()} items in store.")


def show_available_products_for_order(store_instance, reserved_quantities):
    """
    Show available products with their remaining quantities.
    """
    # Init a list of tuples (available_product, quantity_available)
    available_products = []

    for product in store_instance.get_active_products():
        reserved = reserved_quantities.get(product, 0)

        if isinstance(product, products.NonStockedProduct):
            # No quantity needed: Non-Stocked-Product
            available_products.append((product, None))

        elif reserved < product.quantity:
            qty_available = product.quantity - reserved
            available_products.append((product, qty_available))

    if not available_products:
        return []

    print("-" * 10)
    for i, (product, qty_available) in enumerate(available_products, start=1):
        if isinstance(product, products.NonStockedProduct):
            # <print(product)> calls <str(product)> of class NonStockedProduct(Product) (see: products.py)
            print(f"{i} {product}")

        elif isinstance(product, products.LimitedProduct):
            print(
                f"{i}. {product.name}, Price: {product.price}, "
                f"Quantity: {qty_available} (Max per order: {product.max_quantity})"
                f"{product.promo_text()}"
            )

        else:
            print(f"{i}. {product.name}, Price: {product.price}, Quantity: {qty_available}{product.promo_text()}")
    print("-" * 10)

    # Return list of only products because in make_order() user will choose from this list by index number
    return [product for product, _ in available_products]


def make_order(store_instance):
    """
    This function takes care of making an order.
    """
    reserved_quantities = {}

    print("\nTo FINISH your order, press ENTER.")
    print("To CANCEL your order, enter 'q'.")

    while True:
        # Create a list of available products and show available products before each selection
        available_products = show_available_products_for_order(store_instance, reserved_quantities)

        if not available_products:
            print_framed_message("EVERYTHING IS SOLD OUT!")
            break

        user_order = input("\nEnter the product # you want: ").strip()

        if user_order == "".strip():
            break

        if user_order.lower().strip() == "q":
            print("ORDER CANCELLED.")
            return

        if not user_order.isdigit() or not (1 <= int(user_order) <= len(available_products)):
            print("Invalid choice. Try again.")
            continue

        product_nr = int(user_order) - 1
        product = available_products[product_nr]

        while True:
            amount = input("Enter the amount you want: ").strip()

            if amount == "".strip():
                break

            if amount.lower().strip() == "q":
                print("ORDER CANCELLED.")
                return

            if not amount.isdigit():
                print("Please enter a valid number for the amount.")
                continue

            amount = int(amount)

            if isinstance(product, products.LimitedProduct):
                if amount > product.max_quantity:
                    print(f"The maximum quantity you can buy is {product.max_quantity}.")
                    continue

            # Get quantity of reserved product and store in variable 'reserved'
            reserved = reserved_quantities.get(product, 0)
            if not isinstance(product, products.NonStockedProduct):
                # Check how much available to order based on reserved products
                available_to_order = product.quantity - reserved
                if amount <= 0 or amount > available_to_order:
                    print(f"Please enter an amount between 1 and {available_to_order}.")
                    continue

            # Update reserved quantities and add to shopping list
            reserved_quantities[product] = reserved + amount
            break

        current_total = 0
        # print(f"RESERVED: {reserved_quantities}")
        for product, qty in reserved_quantities.items():
            current_total += product.calculate_price(qty)
        print(f"Your current total is {current_total}")

        # Check if product now sold out (based on reserved)
        if not isinstance(product, products.NonStockedProduct):
            if reserved_quantities.get(product, 0) == product.quantity:
                print_framed_message(f"{product.name} is now SOLD OUT!")

    if reserved_quantities:
        shopping_list = list(reserved_quantities.items())
        # print(f"SHOPPING LIST: {shopping_list}")
        print_framed_message(f"Order made! Total payment {store_instance.order(shopping_list)}")


def print_framed_message(message: str, pad: int = 4):
    """
    Print any message framed with asterisks, padded and centered.
    """
    lines = message.split("\n")
    max_length = max(len(line) for line in lines)
    width = max_length + pad * 2
    border = "*" * (width + 2)


    print(border)
    for line in lines:
        print("*" + line.center(width) + "*")
    print(border)


def exit_store():
    """
    Exit the program.
    """
    print("GOODBYE!")


def main():
    """Main function starts the program"""
    # setup initial stock of inventory
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250),
        products.NonStockedProduct("Windows License", price=125),
        products.LimitedProduct("Shipping", price=10, quantity=250, max_quantity=1)
    ]

    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].add_promo(second_half_price)
    product_list[1].add_promo(third_one_free)
    product_list[3].add_promo(thirty_percent)

    # create Store instance
    best_buy = store.Store(product_list)
    start(best_buy)


if __name__ == "__main__":
    main()

