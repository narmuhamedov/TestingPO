import pytest
from bank_limit import calculate_free


@pytest.mark.parametrize(
    "amount, expected_free, description",
    [
        (0,      0.0,   'Нижняя граница бесплатной зоны'),
        (500,    0.0,   'Внутри бесплатной зоны'),
        (1000,   0.0,   'Верхняя граница бесплатной зоны'),

        (1001,   10.01, 'Нижняя граница комиссионной зоны'),
        (25000,  250.0, 'Внутри зоны с комиссией'),
        (50000,  500.0, 'Верхняя граница комиссионной зоны'),

        (50001,  -2.0,  'Граница превышения лимита'),
        (100000, -2.0,  'Заведомое превышение лимита'),

        (-1,     -1.0,  'Негативная сумма перевода'),
    ],
    ids=lambda p: f"Amount_{p}_".replace(" ", "_"),   # p — это кортеж (amount, expected, description)
)
def test_free_matrix(amount, expected_free, description):
    assert calculate_free(amount) == expected_free


def test_invalid_type_exception():
    with pytest.raises(TypeError):
        calculate_free('тысяча сом')