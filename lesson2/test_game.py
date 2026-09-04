from game_logic import get_event, add_coins, is_game_finished
import pytest

# def test_invalid_event():
#     with pytest.raises(ValueError):
#         get_event()

def test_game_not_finished():
    assert is_game_finished(5) ==  False

def test_game_finished():
    assert is_game_finished(11) == True

def test_add_10_coins():
    assert add_coins(0,10) == 10

def test_add_coins_to_existing():
    assert add_coins(20,10) == 30


# def test_monster():
#     assert get_event(1) == 'monster'


# def test_coins():
#     assert get_event(2) == 'coins'

# def test_empty_room():
#     assert get_event(3) == 'empty'


# def test_add_coins():
#     assert add_coins(0, 10)== 10

# def test_add_coins_to_existing_coins():
#     assert add_coins(20,10) == 30