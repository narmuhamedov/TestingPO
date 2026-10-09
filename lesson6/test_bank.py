import pytest
from bank import BankAccount, InsufficientFundsError

class TestBankAccount:
    @pytest.fixture(autouse=True)
    def setup_account(self):
        self.account = BankAccount(owner='Алексей А.', initial_balance=100.0)


    def test_initial_balance(self):
        assert self.account.balance==100.0
        assert self.account.owner == 'Алексей А.'

    def test_deposit_success(self):
        new_balance = self.account.deposit(50.0)
        assert new_balance == 150.0
        assert self.account.balance == 150.0

    def test_deposit_negative_amount_raises_error(self):
        with pytest.raises(ValueError, match='Сумма пополнения должна быть не меньше 1'):
            self.account.deposit(-20)

    def test_withdraw_success(self):
        new_balance = self.account.withdraw(40.0)
        assert new_balance == 60.0
        assert self.account.balance == 60.0

    def test_withdraw_insufficient_funds_raises_error(self):
        with pytest.raises(InsufficientFundsError, match='не достаточно средств на счету'):
            self.account.withdraw(150.0)