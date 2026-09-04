import random

room = 1
coins = 0
while room <= 10:
    print()
    print('Ты вошел в комнату', room)

    event = random.randint(1,3)

    if event == 1:
        print('На тебя напал монстр👹')
        print('Ты убежал!😬')
    elif event == 2:
        print('🤑 ты нашел 10 монет')
        coins += 10
    else:
        print('🙄 комната пустая!')

    room +=1

print()
print('🧭 Ты прошел все комнаты')
print(f"👑 ты собрал монет - {coins}")

