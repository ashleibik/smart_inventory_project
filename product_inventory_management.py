
from product import Product

# ---------------- File I/O ----------------

def load_products(filename):
    products = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.lower().startswith("id,"):
                    # skip header or empty
                    continue
                parts = line.split(",")
                if len(parts) < 6:
                    # not enough fields
                    continue
                pid = parts[0].strip()
                name = parts[1].strip()
                try:
                    category = int(parts[2].strip())
                    qty = int(parts[3].strip())
                    price = float(parts[4].strip())
                    reorder = int(parts[5].strip())
                except:
                    # skip invalid lines
                    continue
                products.append(Product(pid, name, category, qty, price, reorder))
    except FileNotFoundError:
        # start with empty list if file not found
        products = []
    return products


def save_products(filename, products):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("ID,Name,Category Index,Quantity,Price,Reorder Level\n")
        for p in products:
            f.write(",".join([
                p.get_product_id(),
                p.get_name(),
                str(p.get_category()),
                str(p.get_quantity()),
                f"{p.get_price():.2f}",
                str(p.get_reorder_level())
            ]) + "\n")


# ---------------- UI Helpers ----------------

def print_menu():
    print("\n=== Smart Inventory Management ===")
    print("1) List all products")
    print("2) Search products")
    print("3) Add product")
    print("4) Remove product")
    print("5) Edit product")
    print("6) Sell product")
    print("7) Restock product")
    print("8) Low stock report")
    print("9) Inventory summary")
    print("10) List by category")
    print("0) Save & Exit")
    choice = input("Select an option: ").strip()
    return choice


def product_index(products, product_id):
    for i in range(len(products)):
        if products[i].get_product_id().lower() == product_id.lower():
            return i
    return -1


def print_products(products):
    if len(products) == 0:
        print("(no products)")
        return
    print("{:<8} {:<20} {:<12} {:>8} {:>10} {:>14}".format(
        "ID", "Name", "Category", "Qty", "Price", "ReorderLvl"
    ))
    print("-" * 74)
    for p in products:
        print("{:<8} {:<20} {:<12} {:>8} {:>10} {:>14}".format(
            p.get_product_id(),
            p.get_name(),
            p.get_category_name(),
            p.get_quantity(),
            f"{p.get_price():.2f}",
            p.get_reorder_level()
        ))


def _input_nonempty(prompt):
    text = input(prompt).strip()
    return text


def _input_int(prompt):
    # allow up to 3 attempts, with a clear loop condition
    for _ in range(3):
        text = input(prompt).strip()
        try:
            return int(text)
        except:
            print("Please enter a valid integer.")
    print("Too many invalid attempts.")
    return None


def _input_float(prompt):
    for _ in range(3):
        text = input(prompt).strip()
        try:
            return float(text)
        except:
            print("Please enter a valid number (e.g., 12.50).")
    print("Too many invalid attempts.")
    return None


def search_product(products, term):
    term_low = term.lower()
    found = []
    for p in products:
        if term_low in p.get_name().lower() or term_low in p.get_category_name().lower():
            found.append(p)
    return found


def add_product(products):
    pid = _input_nonempty("Enter product ID: ")
    if product_index(products, pid) != -1:
        print("ID already exists.")
        return
    name = _input_nonempty("Enter product name: ")
    category = _input_int("Enter category index (0-9): ")
    if category is None or category < 0 or category > 9:
        print("Invalid category index.")
        return
    qty = _input_int("Enter quantity (integer): ")
    if qty is None:
        return
    price = _input_float("Enter price (e.g., 19.99): ")
    if price is None:
        return
    reorder = _input_int("Enter reorder level (integer): ")
    if reorder is None:
        return
    products.append(Product(pid, name, category, qty, price, reorder))
    print("Product added.")


def remove_product(products):
    pid = _input_nonempty("Enter product ID to remove: ")
    idx = product_index(products, pid)
    if idx == -1:
        print("Product not found.")
        return
    products.pop(idx)
    print("Product removed.")


def edit_product(products):
    pid = _input_nonempty("Enter product ID to edit: ")
    idx = product_index(products, pid)
    if idx == -1:
        print("Product not found.")
        return
    p = products[idx]
    print("Leave a field empty to keep current value.")
    name = input(f"New name [{p.get_name()}]: ").strip()
    if name != "":
        p.set_name(name)
    cat_txt = input(f"New category index (0-9) [{p.get_category()}]: ").strip()
    if cat_txt != "":
        try:
            cat_val = int(cat_txt)
            if 0 <= cat_val <= 9:
                p.set_category(cat_val)
            else:
                print("Invalid category index; keeping old.")
        except:
            print("Invalid category index; keeping old.")
    price_txt = input(f"New price [{p.get_price():.2f}]: ").strip()
    if price_txt != "":
        try:
            p.set_price(float(price_txt))
        except:
            print("Invalid price; keeping old.")
    rl_txt = input(f"New reorder level [{p.get_reorder_level()}]: ").strip()
    if rl_txt != "":
        try:
            p.set_reorder_level(int(rl_txt))
        except:
            print("Invalid reorder level; keeping old.")
    print("Product updated.")


def sell_product(products):
    pid = _input_nonempty("Enter product ID to sell: ")
    idx = product_index(products, pid)
    if idx == -1:
        print("Product not found.")
        return
    amount = _input_int("Enter quantity to sell: ")
    if amount is None:
        return
    ok = products[idx].sell(amount)
    if ok:
        print("Sale successful.")
    else:
        print("Not enough stock or invalid amount.")


def restock_product(products):
    pid = _input_nonempty("Enter product ID to restock: ")
    idx = product_index(products, pid)
    if idx == -1:
        print("Product not found.")
        return
    amount = _input_int("Enter restock amount: ")
    if amount is None:
        return
    ok = products[idx].restock(amount)
    if ok:
        print("Restocked successfully.")
    else:
        print("Invalid restock amount.")


def low_stock_report(products):
    lows = []
    for p in products:
        if p.needs_restock():
            lows.append(p)
    if len(lows) == 0:
        print("No products below reorder level.")
    else:
        print("=== Low Stock Items ===")
        print_products(lows)


def inventory_summary(products):
    total_products = len(products)
    total_qty = 0
    for p in products:
        total_qty += p.get_quantity()
    print(f"Total number of products: {total_products}")
    print(f"Total quantity of all products: {total_qty}")


def list_products_by_category(products):
    cat = _input_int("Enter category index (0-9): ")
    if cat is None or cat < 0 or cat > 9:
        print("Invalid category index.")
        return
    filtered = []
    for p in products:
        if p.get_category() == cat:
            filtered.append(p)
    if len(filtered) == 0:
        print("No products in selected category.")
    else:
        print_products(filtered)


def main():
    filename = "inventory.csv"
    products = load_products(filename)

    choice = ""  # loop ends when choice == "0"
    while choice != "0":
        choice = print_menu()
        if choice == "1":
            print_products(products)
        elif choice == "2":
            term = _input_nonempty("Enter name or category to search: ")
            found = search_product(products, term)
            if len(found) == 0:
                print("No matches.")
            else:
                print_products(found)
        elif choice == "3":
            add_product(products)
        elif choice == "4":
            remove_product(products)
        elif choice == "5":
            edit_product(products)
        elif choice == "6":
            sell_product(products)
        elif choice == "7":
            restock_product(products)
        elif choice == "8":
            low_stock_report(products)
        elif choice == "9":
            inventory_summary(products)
        elif choice == "10":
            list_products_by_category(products)
        elif choice == "0":
            save_products(filename, products)
            print("Saved. Goodbye!")
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
