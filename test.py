import unittest
from api import Bar, Shelves, Inventories, Ingredients

class TestApp(unittest.TestCase):
    def test_bar_order_by_name(self):
        result = Bar().order_by_name("margarita")

        self.assertEqual()




if __name__ == '__main__':
    unittest.main()



class TestSum(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()