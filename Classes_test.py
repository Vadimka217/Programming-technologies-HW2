import pytest
from Classes import Ingredient, Recipe, ShoppingList, DietaryRecipe

def test_ingredient_creation():
    ing = Ingredient("Мука", 500.0, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500.0
    assert ing.unit == "г"

def test_ingredient_str():
    ing = Ingredient("Мука", 500.0, "г")
    result = str(ing)
    assert result == "Мука: 500.0 г"

def test_ingredient_eq_same_name_and_unit():
    ing1 = Ingredient("Мука", 500.0, "г")
    ing2 = Ingredient("Мука", 1000.0, "г")
    assert ing1 == ing2

def test_ingredient_eq_different_name():
    ing1 = Ingredient("Мука", 500.0, "г")
    ing2 = Ingredient("Сахар", 500.0, "г")
    assert ing1 != ing2

def test_ingredient_eq_different_unit():
    ing1 = Ingredient("Мука", 500.0, "г")
    ing2 = Ingredient("Мука", 500.0, "кг")
    assert ing1 != ing2

def test_ingredient_quantity_validation():
    ing = Ingredient("Мука", 500.0, "г")
    with pytest.raises(ValueError, match="Количество должно быть положительным"):
        ing.quantity = -10


def test_recipe_creation():
    ing = Ingredient("Мука", 500.0, "г")
    recipe = Recipe("Пицца", [ing])
    assert recipe.title == "Пицца"
    assert len(recipe) == 1

def test_recipe_add_ingredient_new():
    recipe = Recipe("Пицца")
    ing = Ingredient("Мука", 500.0, "г")
    recipe.add_ingredient(ing)
    assert len(recipe) == 1
    assert recipe.ingredients[0].quantity == 500.0

def test_recipe_add_ingredient_duplicate():
    recipe = Recipe("Пицца")
    ing1 = Ingredient("Мука", 500.0, "г")
    ing2 = Ingredient("Мука", 200.0, "г")
    recipe.add_ingredient(ing1)
    recipe.add_ingredient(ing2)
    assert len(recipe) == 1
    assert recipe.ingredients[0].quantity == 700.0

def test_recipe_scale_returns_new_object():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500.0, "г")])
    scaled = recipe.scale(2.0)
    assert recipe.ingredients[0].quantity == 500.0
    assert scaled.ingredients[0].quantity == 1000.0

def test_recipe_scale_invalid_ratio():
    recipe = Recipe("Пицца")
    with pytest.raises(ValueError):
        recipe.scale(0)
    with pytest.raises(ValueError):
        recipe.scale(-5)

def test_recipe_len():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500.0, "г"))
    recipe.add_ingredient(Ingredient("Сахар", 10.0, "г"))
    recipe.add_ingredient(Ingredient("Мука", 100.0, "г"))
    assert len(recipe) == 2


def test_shopping_list_add_recipe():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500.0, "г")])
    shop_list = ShoppingList()
    shop_list.add_recipe(recipe, 2.0)
    items = shop_list.get_list()
    assert len(items) == 1
    assert items[0].quantity == 1000.0

def test_shopping_list_add_recipe_invalid_portions():
    recipe = Recipe("Пицца")
    shop_list = ShoppingList()
    with pytest.raises(ValueError, match="положительным"):
        shop_list.add_recipe(recipe, 0)

def test_shopping_list_remove_recipe():
    recipe1 = Recipe("Пицца", [Ingredient("Мука", 500.0, "г")])
    recipe2 = Recipe("Торт", [Ingredient("Сахар", 200.0, "г")])
    shop_list = ShoppingList()
    shop_list.add_recipe(recipe1, 1.0)
    shop_list.add_recipe(recipe2, 1.0)
    shop_list.remove_recipe("Пицца")
    items = shop_list.get_list()
    assert len(items) == 1
    assert items[0].name == "Сахар"

def test_shopping_list_remove_nonexistent_recipe():
    shop_list = ShoppingList()
    shop_list.remove_recipe("Несуществующий")
    assert True

def test_shopping_list_merge_same_ingredients():
    recipe1 = Recipe("Пицца", [Ingredient("Мука", 500.0, "г")])
    recipe2 = Recipe("Хлеб", [Ingredient("Мука", 300.0, "г")])
    shop_list = ShoppingList()
    shop_list.add_recipe(recipe1, 1.0)
    shop_list.add_recipe(recipe2, 1.0)
    items = shop_list.get_list()
    assert len(items) == 1
    assert items[0].quantity == 800.0

def test_shopping_list_get_list_sorted():
    recipe = Recipe("Сборная", [
        Ingredient("Яйца", 3, "шт"),
        Ingredient("Мука", 500.0, "г"),
        Ingredient("Сахар", 200.0, "г")
    ])
    shop_list = ShoppingList()
    shop_list.add_recipe(recipe, 1.0)
    items = shop_list.get_list()
    names = [item.name for item in items]
    assert names == sorted(names)

def test_shopping_list_add():
    recipe1 = Recipe("Пицца", [Ingredient("Мука", 500.0, "г")])
    recipe2 = Recipe("Хлеб", [Ingredient("Сахар", 200.0, "г")])
    list1 = ShoppingList()
    list2 = ShoppingList()
    list1.add_recipe(recipe1, 1.0)
    list2.add_recipe(recipe2, 1.0)
    combined = list1 + list2
    assert len(combined.get_list()) == 2
    assert len(list1.get_list()) == 1
    assert len(list2.get_list()) == 1