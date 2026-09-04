from lesson1 import add, subtract, multiply, divide

print('КАЛЬКУЛЯТОР')

a = float(input("Введите первое число: "))
operation = input("Введите операцию (+, -, *, /): ")
b = float(input('Введите второе число: '))


if operation == "+":
    result = add(a, b)
elif operation == '-':
    result = subtract(a,b)
elif operation == '*':
    result = multiply(a,b)
elif operation == '/':
    result = divide(a,b)

else:
    print('Неизвестная операция')
    result = None

print(f'Результат: {result}')
