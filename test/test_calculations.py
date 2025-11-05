import pytest

from app.calculations import add, subtract, multiply, divide, BankAccount

@pytest.fixture # runs before each test function that uses it
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (3, 4, 7)
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 0) == 0
    assert subtract(-1, -1) == 0

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-1, 1) == -1
    assert multiply(0, 100) == 0

def test_divide():
    assert divide(6, 3) == 2.0
    assert divide(-6, 2) == -3.0
    with pytest.raises(ValueError):
        divide(5, 0)

def test_bank_set_initial_balance(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_deposit(zero_bank_account):
    zero_bank_account.deposit(50)
    assert zero_bank_account.balance == 50

def test_bank_withdraw(bank_account):
    bank_account.withdraw(30)
    assert bank_account.balance == 20

def test_bank_collect_interest(bank_account):
    bank_account.collect_interest(1.1)
    assert round(bank_account.balance, 4) == 55.0

@pytest.mark.parametrize("deposit, withdraw, interest, expected", [
    (100, 50, 1.2, 60.0),
    (200, 150, 1.1, 55.0),
    (50, 20, 1.05, 31.5)
])

def test_bank_transactions(zero_bank_account, deposit, withdraw, interest ,expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    zero_bank_account.collect_interest(interest)
    assert round(zero_bank_account.balance, 4) == expected

def test_insufficient_funds(zero_bank_account):
    with pytest.raises(ValueError):
        zero_bank_account.withdraw(1000)