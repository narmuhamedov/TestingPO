import pytest

from shop_logic import (
    calculate_price,
    apply_discount,
    add_to_cart,
    calculate_cart_total
)

def test_calculate_price():
    assert calculate_price(1000, 3)==3000

def test_apply_discount():
    assert apply_discount(10000, 10) == 9000

def test_zero_discount():
    assert apply_discount(10000, 0) == 10000

def test_full_discount():
    assert apply_discount(10000, 100) == 0


def test_add_to_cart():
    cart = []

    add_to_cart(cart, "Мышь", 2)

    assert len(cart) == 1
    assert cart[0]['product'] == 'Мышь'
    assert cart[0]['quantity'] == 3

def test_empty_cart():
    cart = []

    products = {
        "Мышь": 1500
    }

    assert calculate_cart_total(cart, products) == 0