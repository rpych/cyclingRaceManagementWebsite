from django.db import models
from django.utils import timezone
# Create your models here.



class Bike(models.Model):
    name = models.CharField(max_length=100)
    est_year = models.CharField(max_length=30,default=timezone.now)
    image = models.ImageField(upload_to='media/', null=True)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name and self.est_year == other.est_year


class Team(models.Model):
    bike_brand = models.ForeignKey(Bike, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    cyclist_amount = models.CharField(max_length=30,default='0')
    est_year = models.CharField(max_length=30,default=timezone.now)
    image = models.ImageField(upload_to='media/', null=True)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name and self.cyclist_amount == other.cyclist_amount and self.est_year == other.est_year



class Person(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birthDate = models.CharField(null=True, max_length=100)
    image = models.ImageField(upload_to='media/', null=True)

    def __str__(self):
        return self.name + ' ' + self.surname

    def __eq__(self, other):
        return self.surname == other.surname and self.name == other.name and self.birthDate == other.birthDate and self.phone_number == other.phone_number and self.email == other.email


class Stage(models.Model):
    start_city = models.CharField(max_length=100)
    finish_city = models.CharField(max_length=100)
    kilometers = models.CharField(max_length=30)
    difficulty = models.IntegerField(default=1)
    image = models.ImageField(upload_to='media/', null=True)


    def __str__(self):
        return str(self.id) + '. ' + self.start_city + '-' + self.finish_city + ' ' + self.kilometers + ' km' 