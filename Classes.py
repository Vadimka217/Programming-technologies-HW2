class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self._quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(value)

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit

class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        if ingredients is None:
            self.ingredients = []
        else:
            self.ingredients = ingredients

    def add_ingredient(self, ingredient):
        for i in self.ingredients:
            if i == ingredient:
                i.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        return ratio > 0 and isinstance(ratio, (int, float))

    def scale(self, ratio):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным числом")
        scaled_ingredients = []
        for ing in self.ingredients:
            new_quantity = ing.quantity * ratio
            scaled_ing = Ingredient(ing.name, new_quantity, ing.unit)
            scaled_ingredients.append(scaled_ing)
        return Recipe(self.title, scaled_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        if not self.ingredients:
            return f"{self.title}: Ингредиенты отсутствуют"
        ingredients_str = "\n".join(f"  - {ing}" for ing in self.ingredients)
        return f"{self.title}:\n{ingredients_str}"
