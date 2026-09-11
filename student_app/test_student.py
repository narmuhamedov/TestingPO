from student_service import add_student

def test_add_student():
    student = add_student(
        "Ivan",
        'Ivanov',
        20,
        85
    )

    assert student['name'] == 'Ivan'
    assert student['surname'] == 'Ivanov'
    assert student['age'] == 20
    assert student['score'] == 85