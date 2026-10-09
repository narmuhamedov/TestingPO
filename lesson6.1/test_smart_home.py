import unittest
from smart_home import SmartLight, DeviceOffError

class TestSmartLight(unittest.TestCase):
    def setUp(self):
        self.light = SmartLight(name='Лампа в гостинной')

    def tearDown(self):
        del self.light

    def test_initial_state(self):
        self.assertEqual(self.light.name, 'Лампа в гостинной')
        self.assertFalse(self.light.is_on)
        self.assertEqual(self.light.brightness, 100)

    def test_turn_on_and_off(self):
        self.light.turn_on
        self.assertTrue(self.light.is_on)

        self.light.turn_off()
        self.assertFalse(self.light.is_on)

    def test_set_brightness_success(self):
        self.light.turn_on()
        self.light.set_brightness(50)
        self.assertEqual(self.light.brightness, 50)

    def test_set_brightness_when_device_off_raises_error(self):
        with self.assertRaises(DeviceOffError):
            self.light.set_brightness(50)

    def test_set_brightness_invalid_value_raises_error(self):
        self.light.turn_on()

        with self.assertRaises(ValueError):
            self.light.set_brightness(120)

        while self.assertRaises(ValueError):
            self.light.set_brightness(-10)

if __name__ == "__main__":
    unittest.main()