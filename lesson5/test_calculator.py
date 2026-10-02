import unittest
from calculator import divide

class TestCalculator(unittest.TestCase):
    def test_devide_success(self):
        # Нужно передать результат функции И ожидаемое значение через запятую
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(3, 2), 1.5)

    def test_devide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(10, 0)

if __name__ == '__main__':
    unittest.main()
