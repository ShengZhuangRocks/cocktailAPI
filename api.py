"""
Basically the API is treated as a pub,

with Inventories() of all categories, glasses, ingredients and alcoholic items,
which just provide lists of general categories of all items;

and we have Shelves() to showcase all bottles and glasses,
which provide a summary list of drinks and ingredients

now at the Bar(), the bartender serves you all kinds of drinks,
which provide detail information of selected drink/drinks

this API also provide Ingredients() for searching ingredients details
"""

import requests


class Bar:
    """
    Drinks ready to be served on the bar, presented by the bartender in detail
    example:
    --------
    # searching the API first, then parsing the data back
    Bar().order_by_name("margarita").get_drinks_details()
    """

    def __init__(self):
        self.data = None

    # searching data from the API
    def order_by_name(self, key):
        """
        :param  key: drink name, like "margarita"
        :return list of dict items, full recipe of the drinks
        """
        path = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s=" + key
        self.data = requests.get(path).json()["drinks"]
        # print(json.dumps(self.data, indent=4, sort_keys=True))
        return self

    def order_by_first_letter(self, key):
        """
        :param  key: first letter of drink name
        :return list of dict items, full recipe of the drinks
        """
        path = "https://www.thecocktaildb.com/api/json/v1/1/search.php?f=" + key
        self.data = requests.get(path).json()["drinks"]
        return self

    def order_by_drink_id(self, drink_id):
        """
        :param  drink_id
        :return list with single dict item, full recipe of a drink
        """
        path = "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=" + str(drink_id)
        self.data = requests.get(path).json()["drinks"]
        return self

    def order_a_random_drink(self):
        """
        :return: single dict item, full recipe of a drink
        """
        path = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
        self.data = requests.get(path).json()["drinks"]
        return self

    # using the retrieving data to find drink details
    def get_drink_names(self):
        drink_names = [drink["strDrink"] for drink in self.data]
        # sometime when the result has only one item,
        # it just makes more sense to return the item instead of a list.
        if len(drink_names) == 1:
            drink_names = drink_names[0]
        return drink_names

    def get_drink_details(self):
        drinks_details = []
        for drink in self.data:
            drink_sorted = {
                "drink_id": drink["idDrink"],
                "drink_name": drink["strDrink"],
                "glass": drink["strGlass"],
                "ingredients": {},
                "instruction": drink["strInstructions"]
                # Todo, add more key value pairs
            }
            # make ingredients pair up with measures
            for i in range(1, 15):
                ingredient = drink[f"strIngredient{i}"]
                measure = drink[f"strMeasure{i}"]
                if ingredient is None:
                    break
                if measure is None:
                    measure = "a tiny winy bit"
                drink_sorted["ingredients"][ingredient] = measure
            drinks_details.append(drink_sorted)
        # sometime when the result has only one item,
        # it just makes more sense to return the item instead of a list.
        if len(drinks_details) == 1:
            drinks_details = drinks_details[0]
        return drinks_details


class Shelves:
    """
    All bottles on the selves, provide a general look of all drinks and ingredients
    """
    def __init__(self):
        self.data = None

    # searching API
    def filter_by_ingredient(self, key):
        """
        :param key: ingredient name
        :return: list of dict items, with id, name and thumbnail
        """
        path = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=" + key
        self.data = requests.get(path).json()["drinks"]
        return self

    def filter_by_type(self, key):
        """
        :param key: Alcoholic/Non-Alcoholic, Ordinary_Drink/Cocktail/or other drinks types,
        check Inventory() for more drinks types
        :return: list of dict items, with id, name and thumbnail
        """
        if "alcohol" in key.lower():
            path = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=" + key
            self.data = requests.get(path).json()["drinks"]
            return self
        else:
            path = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?c=" + key
            self.data = requests.get(path).json()["drinks"]
            return self

    def filter_by_container(self, key):
        """
        :param key: container of the drink, you can check Inventory() for containers types
        :return:
        """
        path = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?g=" + key
        self.data = requests.get(path).json()["drinks"]
        return self

    def get_names(self):
        return [drink["strDrink"] for drink in self.data]


class Inventories:
    """
    check the Inventory for all categories, glasses, ingredients and alcoholic items
    :key "C" for categories/"g" for glass/"i" for ingredients/"a" for alcoholic types
    :return a list of all glasses for example, or categories/ingredients/alcoholic

    example:
    --------
    Inventory("a").data

    """
    def __init__(self, key):
        if "c" in key.lower():
            path = "https://www.thecocktaildb.com/api/json/v1/1/list.php?c=list"
            print("searching inventory for all categories")
            self.data = requests.get(path).json()["drinks"]
            self.data = [d["strCategory"] for d in self.data]
        elif "g" in key.lower():
            path = "https://www.thecocktaildb.com/api/json/v1/1/list.php?g=list"
            print("searching inventory for all glass")
            self.data = requests.get(path).json()["drinks"]
            self.data = [d["strGlass"] for d in self.data]
        elif "i" in key.lower():
            path = "https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list"
            print("searching inventory for all ingredients")
            self.data = requests.get(path).json()["drinks"]
            self.data = [d["strIngredient1"] for d in self.data]
        elif "a" in key.lower():
            path = "https://www.thecocktaildb.com/api/json/v1/1/list.php?a=list"
            print("searching inventory for all alcoholic/other types")
            self.data = requests.get(path).json()["drinks"]
            self.data = [d["strAlcoholic"] for d in self.data if d["strAlcoholic"] is not None]
        else:
            print("No such item in the inventory")


class Ingredients:
    """
    find ingredient details
    : key_type  "name" ingredient name/ "id" ingredient id
    :return  dictionary of the item, or list of dict items

    example:
    --------
    Ingredients("gin").data
    Ingredients("gin").get_recipes_list()
    """
    def __init__(self, key, key_type="name"):
        self.key = key
        self.key_type = key_type
        if self.key_type == "name":
            path = "https://www.thecocktaildb.com/api/json/v1/1/search.php?i=" + key
            self.data = requests.get(path).json()["ingredients"]
            if len(self.data) == 1:
                self.data = self.data[0]
        elif self.key_type == "id":
            path = "https://www.thecocktaildb.com/api/json/v1/1/search.php?iid=" + key
            self.data = requests.get(path).json()["ingredients"]
            if len(self.data) == 1:
                self.data = self.data[0]

    def get_recipes_list(self):
        if self.key_type == "name":
            path = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=" + self.key
            return requests.get(path).json()["drinks"]
