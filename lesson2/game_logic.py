def get_event(event):
    if event == 1:
        return 'monster'
    elif event == 2:
        return 'coins'
    elif event == 3:
        return 'empty'
    else:
        raise ValueError('Событие должно быть от 1 до 3')


print(get_event(1))
print(get_event(2))
print(get_event(3))

def add_coins(coins, amount):
    return coins + amount

def is_game_finished(room):
    return room > 10