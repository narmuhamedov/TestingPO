import unittest
from shopping_cart import ShoppingCart

class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def tearDown(self):
        del self.cart

    def test_empty_cart_total(self):
        self.assertEqual(self.cart.get_total(),0)

    def test_add_item(self):
        self.cart.add_item('Книга', 500)
        self.assertEqual(len(self.cart.items),1)
        self.assertEqual(self.cart.get_total(), 500)

    def test_multiple_items_total(self):
        self.cart.add_item('Ручка',50)
        self.cart.add_item('Тетрадь',100)
        self.assertEqual(self.cart.get_total(),150)
                