from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from otnosheniye.models import Car, CategoryCar, StateNumberCar, CommentCar


class CarAppTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = CategoryCar.objects.create(name='Седан')

        self.car1 = Car.objects.create(
            title='BMW E34',
            vin_code='WWWZZZYYY123333',
            person='Иванов Иван',
            description='Good Car'
        )
        self.car1.categories.add(self.category)

        self.car2 = Car.objects.create(
            title='Volkwagen GOLF5',
            vin_code='WWWZZZYYY123321',
            person='Lenova Leona',
            description='Good Car Vau'
        )

        self.state_number = StateNumberCar.objects.create(
            car_choice=self.car1,
            number_car="01KG888AAA"
        )

        self.comment = CommentCar.objects.create(
            choice_car=self.car1,
            description='хорошая машина',
            mark=5
        )

    def test_category_car_str(self):
        self.assertEqual(str(self.category), "Седан")

    def test_car_defaults_and_str(self):
        expected_str = f'{self.car1.title}-{self.car1.vin_code}-{self.car1.person}'
        self.assertEqual(str(self.car1), expected_str)

        default_car = Car.objects.create()
        self.assertEqual(default_car.title, "BMW E34")
        self.assertEqual(default_car.vin_code, 'WWWZZZYYY123333')
        self.assertEqual(default_car.person, 'Иванов Иван')

    def test_state_number_car_str(self):
        expected_str = f'{self.car1}-{self.state_number.number_car}'
        self.assertEqual(str(self.state_number), expected_str)

    def test_comment_car_validators(self):
        expected_str = f'{self.car1}-{self.comment.mark}'
        self.assertEqual(str(self.comment), expected_str)

        invalid_comment = CommentCar(choice_car=self.car1, mark=6)
        with self.assertRaises(ValidationError):
            invalid_comment.full_clean()

    def test_car_list_view_status_code(self):
        response = self.client.get(reverse('carsList'))
        self.assertEqual(response.status_code, 200)

    def test_car_list_view_ordering(self):
        response = self.client.get(reverse('carsList'))
        self.assertIn('car', response.context)

        cars = list(response.context['car'])
        self.assertEqual(cars[0], self.car2)
        self.assertEqual(cars[1], self.car1)

    def test_template_content_rendering(self):
        response = self.client.get(reverse('carsList'))
        html = response.content.decode('utf-8')

        self.assertIn('Volkwagen GOLF4', html)
        self.assertIn('WWWZZZYYY123333', html)
        self.assertIn('Lenov Leon', html)
        self.assertIn('Седан', html)
        self.assertIn('Good Car Vau Vau', html)