from django.db import models

#Category many To many
class CategoryCar(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Car(models.Model):
    title = models.CharField(max_length=100, default='BMW E34')
    vin_code = models.CharField(max_length=100, default="WWWZZZYYY123321")
    person = models.CharField(max_length=100, default='Иванов Иван')
    description = models.TextField(max_length=100, blank=True)
    created_at = models.DateField(auto_now_add=True)
    categories = models.ManyToManyField(CategoryCar, null=True)

    def __str__(self):
        return f'{self.title}-{self.vin_code}{self.person}'

#1 к 1
class StateNumberCar(models.Model):
    car_choice = models.OneToOneField(Car, on_delete=models.CASCADE)
    number_car = models.CharField(max_length=100, default="0_KG______")

    def __str__(self):
        return f'{self.car_choice}-{self.number_car}'


from django.core.validators import MaxValueValidator, MinValueValidator
#1 ко многим
class CommentCar(models.Model):
    choice_car = models.ForeignKey(Car, on_delete=models.CASCADE)
    description = models.TextField(default='хорошая машина')
    mark = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), 
                                                              MaxValueValidator(5)])
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.choice_car}-{self.mark}'