from shop_logic import calculate_price, apply_discount, add_to_cart, calculate_cart_total

products = {
    "Ноубук": 70000,
    "Мышь": 1500,
    "Клавиатура": 3000
}

cart = []

print('====================')
print('--------Интернет магазин------')
print('====================')

print("Товары:")
for product, price in products.items():
    print(product, '-', price, "сом")

print()
print('Добавили в корзину')


add_to_cart(cart, 'Ноубук', 1)
add_to_cart(cart, 'Мышь', 2)

for item in cart:
    print(item['product'], "x", item['quantity'])


total = calculate_cart_total(cart, products, )
print()
print("Стоимость", total, 'сом')

discount = 10

final_price = apply_discount(total, discount)

print('Скидка', discount, "%")
print('Итого', final_price, 'сом')