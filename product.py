
class Product:
    # Static categories list (index 0..9)
    _CATEGORIES = [
        "Electronics",
        "Clothing",
        "Home",
        "Grocery",
        "Books",
        "Toys",
        "Sports",
        "Beauty",
        "Automotive",
        "Others",
    ]

    def __init__(self, product_id, name, category, quantity=0, price=0.0, reorder_level=0):
        # Private attributes
        self.__product_id = str(product_id)
        self.__name = str(name)
        self.__category = int(category)  # expects 0..9
        self.__quantity = int(quantity)
        self.__price = float(price)
        self.__reorder_level = int(reorder_level)

    # --------- Getters ---------
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_category(self):
        return self.__category

    def get_quantity(self):
        return self.__quantity

    def get_price(self):
        return self.__price

    def get_reorder_level(self):
        return self.__reorder_level

    # --------- Setters (no setter for quantity) ---------
    def set_product_id(self, product_id):
        self.__product_id = str(product_id)

    def set_name(self, name):
        self.__name = str(name)

    def set_category(self, category):
        self.__category = int(category)

    def set_price(self, price):
        self.__price = float(price)

    def set_reorder_level(self, level):
        self.__reorder_level = int(level)

    # --------- Helpers ---------
    def get_category_name(self):
        idx = self.__category
        if 0 <= idx < len(Product._CATEGORIES):
            return Product._CATEGORIES[idx]
        return "Unknown"

    def needs_restock(self):
        return self.__quantity <= self.__reorder_level

    def restock(self, amount):
        amount = int(amount)
        if amount > 0:
            self.__quantity += amount
            return True
        return False

    def sell(self, amount):
        amount = int(amount)
        if amount <= 0:
            return False
        if self.__quantity >= amount:
            self.__quantity -= amount
            return True
        return False

    def __str__(self):
        # "A001 TV Electronics 10 299.99 $"
        return f"{self.__product_id} {self.__name} {self.get_category_name()} {self.__quantity} {self.__price:.2f} $"
