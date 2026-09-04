def calculate_price(price, quantity):
    return price * quantity

def apply_discount(price, discount):
    if discount < 0 or discount >100:
        raise ValueError('Скидка должна быть от 0 до 100')

    return price - (price * discount / 100)

def add_to_cart(cart, product, quantity):
    if quantity <=0:
        raise ValueError('Кол-во должно быть больше 0')

    cart.append({
        "product": product,
        "quantity": quantity
    })
    return cart

def calculate_cart_total(cart, products):
    total = 0

    for item in cart:
        product = item["product"]
        quantity = item['quantity']

        total += products[product] * quantity
    return total