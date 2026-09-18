def calculate_free(amount:float)->float:
    if not isinstance(amount, (int,float)):
        raise TypeError('Сумма должна быть числом')

    if amount < 0:
        return -1.0

    if amount <=1000:
        return 0.0

    elif amount <=50000:
        return amount * 0.01
    else:
        return -2.0