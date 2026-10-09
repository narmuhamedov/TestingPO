class SmartDevice:
    def __init__(self, name:str):
        self.name = name
        self._is_on = False

    @property
    def is_on(self)->bool:
        return self._is_on

    def turn_on(self):
        self._is_on = True

    def turn_off(self):
        self.is_on = False


class SmartLight(SmartDevice):
    def __init__(self, name:str):
        super().__init__(name)
        self._brightness = 100

    @property
    def brightness(self)-> int:
        return self._brightness

    def set_brightness(self, level:int):
        if not self._is_on:
            raise DeviceOffError('Нельзя регулировать яркость если светильник выключен')
        if not(0<=level<=100):
            raise ValueError('Яркость должна быть в промежутке от 0 до 100')
        self._brightness = level
        


class DeviceOffError(Exception):
    pass