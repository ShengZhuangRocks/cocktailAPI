"""
 DO WHATEVER YOU WANT TO PUBLIC LICENSE
                    Version 1, October 2019

 Copyright (C) 2019 Sheng Zhuang <ShengZh9@gmail.com>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHATEVER YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHATEVER YOU WANT TO.
"""
"""
This app is for talking to the cocktail db API, the free part.
Basically using this API app is like managing a pub,

with Inventories() of all categories, glasses, ingredients and alcoholic items,
which just provide lists of general categories of all items;

and we have Shelves() to showcase all bottles and glasses,
which provide a summary list of drinks and ingredients

now at the Bar(), the bartender serves you all kinds of drinks,
which provide detail information of selected drink/drinks

this API also provide Ingredients() for searching ingredients details
"""


import requests
from json.decoder import JSONDecodeError


class Bar:
    """
    Drinks ready to be served on the bar, presented by the bartender in detail
    example:
    --------
    # searching the API first, then parsing the retrieving data
    Bar().order_by_name("margarita").get_drinks_details()
    """

    def __init__(self):
        self.data = None

    # searching data from the API
    def order_by_name(self, key):
        """
        :param  key: drink name, like "margarita"
        if you not sure what to order, use Shelves() to get list of all drinks
        :return list of dict items, full recipe of the drinks
        """
        try:
            path = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s=" + key
            self.data = requests.get(path).json()["drinks"]
        except JSONDecodeError:
            print("Sorry, no such drink in the API, or check the input again")
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
        try:
            path = "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=" + str(drink_id)
            self.data = requests.get(path).json()["drinks"]
        except JSONDecodeError:
            print("""Sorry, no such drink in the API, the drink id must be 5 digits integer,
                   or use other method to find a proper id.""")
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

    example:
    --------
    Shelves().filter_by_types("Non-Alcoholic").get_names()
    you can use the return data to order a drink at the Bar().
    """
    def __init__(self):
        self.data = None

    # searching API
    def filter_by_ingredient(self, key):
        """
        :param key: ingredient name
        :return: list of dict items, with id, name and thumbnail
        """
        try:
            path = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=" + key
            self.data = requests.get(path).json()["drinks"]
        except JSONDecodeError:
            print("""Sorry, no such ingredient in the API, or check the input again, 
                  or use other Ingredient() to find a proper ingredient.""")

        return self

    def filter_by_type(self, key):
        """
        :param key: Alcoholic/Non-Alcoholic | by categories: Ordinary_Drink/Cocktail/or other drinks types,
        check Inventory().get_categories for more drinks types
        :return: list of dict items, with id, name and thumbnail
        """
        if "alcohol" in key.lower():
            path = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=" + key
            self.data = requests.get(path).json()["drinks"]
            return self
        else:
            try:
                path = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?c=" + key
                self.data = requests.get(path).json()["drinks"]
            except JSONDecodeError:
                print("""Sorry, no such drink type in the API, or check the input again, 
                          or use other Inventories() to find a proper drink type.""")
            return self

    def filter_by_container(self, key):
        """
        :param key: container of the drink, you can check Inventory() for containers types
        :return:
        """
        try:
            path = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?g=" + key
            self.data = requests.get(path).json()["drinks"]
        except JSONDecodeError:
            print("""Sorry, no such container in the API, or check the input again, 
                      or use other Inventories() to find a proper container.""")
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
    Inventory().get_glass_types()

    """
    def __init__(self):
        self.data = None

    def get_categories(self):
        """
        :return: list of categories names
        """
        path = "https://www.thecocktaildb.com/api/json/v1/1/list.php?c=list"
        self.data = requests.get(path).json()["drinks"]
        return [d["strCategory"] for d in self.data]

    def get_container_types(self):
        """
        :return: list of container names
        """
        path = "https://www.thecocktaildb.com/api/json/v1/1/list.php?g=list"
        self.data = requests.get(path).json()["drinks"]
        return [d["strGlass"] for d in self.data]

    def get_drink_types(self):
        """
        :return: list of drink types
        """
        path = "https://www.thecocktaildb.com/api/json/v1/1/list.php?a=list"
        self.data = requests.get(path).json()["drinks"]
        return [d["strAlcoholic"] for d in self.data if d["strAlcoholic"] is not None]


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
    def __init__(self):
        self.data = None
        self.key = None
        self.key_type = None

    def get_all_ingredients(self):
        """
        :return: list of all ingredients
        """
        path = "https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list"
        self.data = requests.get(path).json()["drinks"]
        return [d["strIngredient1"] for d in self.data]

    def get_an_ingredient(self, key, key_type="name"):
        self.key = key
        self.key_type = key_type
        if self.key_type == "name":
            try:
                path = "https://www.thecocktaildb.com/api/json/v1/1/search.php?i=" + key
                self.data = requests.get(path).json()["ingredients"]
                self.data = self.data[0]
            except JSONDecodeError:
                print("""Sorry, no such ingredient in the API, or check the input again, 
                          or use get_all_ingredients to find a proper ingredient.""")

        elif self.key_type == "id":
            try:
                path = "https://www.thecocktaildb.com/api/json/v1/1/search.php?iid=" + str(key)
                self.data = requests.get(path).json()["ingredients"]
                self.data = self.data[0]
            except JSONDecodeError:
                print("""Sorry, no such ingredient in the API, or check the input again, 
                              or use get_all_ingredients to find a proper ingredient.""")
        else:
            print("only name and id is support for checking ingredient.")
            raise ValueError
        return self

    def get_recipes_list(self):
        """
        this method should be used following get_an_ingredient()
        :return: a list of drink recipes that include the exact ingredient
        """
        if self.key_type == "name":
            path = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=" + self.key
            return requests.get(path).json()["drinks"]
        else:
            print("this method should be used following get_an_ingredient().")
            raise ValueError
