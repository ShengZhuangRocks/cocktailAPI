import api

# Bar
marg = api.Bar().order_by_name("margarita").get_drink_details()
d_list = api.Bar().order_by_first_letter("d").get_drink_names()
drink_id = api.Bar().order_by_drink_id(12322).get_drink_details()
random_drink = api.Bar().order_a_random_drink().get_drink_details()

# Shelves
drinks_with_vodka = api.Shelves().filter_by_ingredient("vodka").get_names()
drinks_alcoholic = api.Shelves().filter_by_type("alcoholic").get_names()
drinks_by_champagne_flute = api.Shelves().filter_by_container("Champagne flute").get_names()

# Inventories
all_categories = api.Inventories().get_categories()
all_glass_types = api.Inventories().get_container_types()
alcoholic = api.Inventories().get_drink_types()

# Ingredients
all_ingredients = api.Ingredients().get_all_ingredients()
vodka = api.Ingredients().get_an_ingredient("vodka")
about_vodka = vodka.data
recipes_with_vodka = vodka.get_recipes_list()

