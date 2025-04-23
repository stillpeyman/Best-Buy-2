import products
import promotions
import store


def exit_store():
    """
    Exit the program.
    """
    print("GOODBYE!")


def make_order(store_instance):
    """
    This function takes care of making an order.
    """
    list_all_products(store_instance)

    print("\nTo FINISH your order, press ENTER.")

    shopping_list = []

    while True:
        available_products = []

        # Pre-calculate reserved quantities for all products
        reserved_quantities = {
            product: sum(amount for (p, amount) in shopping_list if p == product)
            for product in store_instance.product_list
        }

        for product in store_instance.product_list:
            if isinstance(product, products.NonStockedProduct):
                available_products.append(product)
                continue

            # Use pre-calculated reserved quantity
            reserved = reserved_quantities.get(product, 0)
            available_qty = product.quantity - reserved

            if available_qty > 0:
                available_products.append(product)

        if not available_products:
            print_framed_message("EVERYTHING IS SOLD OUT!")
            return

        print()
        print("-" * 10)
        for i, product in enumerate(available_products, start=1):
            if isinstance(product, products.NonStockedProduct):
                print(f"{i}. {product.name}, Price: {product.price}{product.promo_text()}")

            elif isinstance(product, products.LimitedProduct):
                # Use pre-calculated reserved quantity
                reserved = reserved_quantities.get(product, 0)
                display_qty = product.quantity - reserved
                print(f"{i}. {product.name}, Price: {product.price}, Quantity: {display_qty} (Max per order: {product.max_quantity}){product.promo_text()}")

            else:
                # Use pre-calculated reserved quantity
                reserved = reserved_quantities.get(product, 0)
                display_qty = product.quantity - reserved
                print(f"{i}. {product.name}, Price: {product.price}, Quantity: {display_qty}{product.promo_text()}")
        print("-" * 10)

        if shopping_list:
            print(f"Your current total is {store_instance.calculate_subtotal(shopping_list)}")

        user_order = input("\nEnter the product # you want to buy (or press ENTER to finish): ").strip()

        if user_order == "":
            break

        if not user_order.isdigit() or not (1 <= int(user_order) <= len(available_products)):
            print("Invalid choice. Try again.")
            continue

        product = available_products[int(user_order) - 1]

        while True:
            amount = input("Enter the quantity you want to buy (or press ENTER to finish): ").strip()

            if amount == "":
                break

            if not amount.isdigit():
                print("Please enter a valid number for the quantity.")
                continue

            amount = int(amount)

            if isinstance(product, products.NonStockedProduct):
                break

            if isinstance(product, products.LimitedProduct):
                if amount > product.max_quantity:
                    print(f"The maximum quantity you can buy is {product.max_quantity}.")
                    continue
                else:
                    break

            # Use pre-calculated reserved quantity
            reserved = reserved_quantities.get(product, 0)
            available_qty = product.quantity - reserved


            if amount <= 0 or amount > product.quantity:
                print(f"Please enter an quantity between 1 and {product.quantity}.")
                continue

            else:
                break

        shopping_list.append((product, amount))

    if shopping_list:
        try:
            total = store_instance.order(shopping_list)
            print_framed_message(f"ORDER MADE! YOUR TOTAL {total}")

            # Check for sold-out items
            for product, _ in shopping_list:
                if product.quantity == 0 and not isinstance(product, products.NonStockedProduct):
                    print_framed_message(f"{product.name} is now SOLD OUT!")

        except Exception as e:
            print(f"Order failed: {e}")


def show_total_quantity(store_instance):
    """
    Show the total number of items in the store.
    """
    print(f"\nTotal of {store_instance.get_total_quantity()} items in store.")


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



def execute_user_choice(store_instance):
    """
    Handle user input and calls corresponding function.
    """
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
            if len(store_instance.get_all_products()) == 0:
                exit_store()
                return

            input("\nPress ENTER to get back to the MENU.")
            print()

        else:
            print("Invalid choice, please try again.")

        start()


def start():
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
    product_list[0].add_promo([second_half_price, third_one_free, thirty_percent])
    product_list[1].add_promo(third_one_free)
    product_list[3].add_promo(thirty_percent)

    # create Store instance
    best_buy = store.Store(product_list)
    start()
    execute_user_choice(best_buy)


if __name__ == "__main__":
    main()

