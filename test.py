import api

marg = api.Bar().order_by_name("margarita").get_drink_details()

d_list = api.Bar().order_by_first_letter("d").get_drink_names()

drink_id = api.Bar().order_by_drink_id(12322).get_drink_details()

random_drink = api.Bar().order_a_random_drink().get_drink_details()

all_categories = api.Inventories("c").data

all_glass_types = api.Inventories("g").data

all_ingredients = api.Inventories("i").data

alcoholic = api.Inventories("a").data

