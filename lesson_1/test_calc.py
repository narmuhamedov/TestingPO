import pytest
from lesson1 import add, subtract, multiply, divide

def test_add():
    assert add(10,5) == 15

def test_subtract():
    assert subtract(-10,5) == 5

def test_multiply():
    assert multiply(10,5) == 50

def test_divide():
    assert divide(10, 0) == 0

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10,5)





# assert add(10, 5) == 15
# assert subtract(10, 5) == 5
# assert multiply (10, 5) == 50
# #assert divide (10, 5) == 2
# divide(10,0)

# print('Все тесты прошли успешно')