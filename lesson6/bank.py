class BankAccount:
    def __init__(self, owner:str, initial_balance:float=0.0):
        self.owner = owner
        self._balace = initial_balance

    @property
    def balance(self) -> float:
        return self._balace

    def deposit(self, amount:float):
        if amount <=0:
            raise ValueError('Сумма пополения должна быть больше 0')
        self._balace += amount
        return self._balace

    def withdraw(self, amount:float) -> float:
        if amount <=0:
            raise ValueError('Сумма для снятия должна быть больше 0')

        self._balace -= amount
        return self._balace

class InsufficientFundsError(Exception):
    pass        