from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class profilepic(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    pic=models.FileField()
    














from django.db import models

class Admen(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # Use hashed passwords in production

    @classmethod
    def authenticate(cls, username, password):
        # Here you should add password hashing and verification
        try:
            user = cls.objects.get(username=username, password=password)
            return user
        except cls.DoesNotExist:
            return None





























# models.py
from django.db import models

class Allocated(models.Model):
    student_name = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=50)
    room = models.CharField(max_length=50)
    bench = models.IntegerField()
    seat = models.IntegerField()
    subject = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    date = models.DateField()  # Corrected here by adding parentheses

    def __str__(self):
        return f"{self.student_name} - Room: {self.room}, Bench: {self.bench}, Seat: {self.seat}"





# webapp/models.py

from django.db import models

class RoomDetails(models.Model):
    user = models.CharField(max_length=100)
    preset_name = models.CharField(max_length=100)
    room_name = models.CharField(max_length=100)
    benches = models.IntegerField()
    seats_per_bench = models.IntegerField()

    def total_seats(self):
        return self.benches * self.seats_per_bench

    def __str__(self):
        return self.room_name
from django.db import models

class Preset(models.Model):
    user = models.CharField(max_length=100)
    preset_name = models.CharField(max_length=100)
    room_name = models.CharField(max_length=100)
    benches = models.IntegerField()
    seats_per_bench = models.IntegerField()




from django.db import models
from django.conf import settings


from django.db import models

class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    reg_no = models.CharField(max_length=50, unique=True)  # Making reg_no unique
    branch = models.CharField(max_length=100)
    semester = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.reg_no})"
