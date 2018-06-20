from django.contrib import admin
from .models import Bike, Team, Person

# Register your models here.
admin.site.register(Bike)
admin.site.register(Team)
admin.site.register(Person)