from django.db import models
from datetime import datetime

# Create your models here.

class Position(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Employee(models.Model):
    fullname = models.CharField(max_length=100)
    emp_code = models.CharField(max_length=3)
    mobile= models.CharField(max_length=15)
    position= models.ForeignKey(Position,on_delete=models.CASCADE)
    is_delete = models.NullBooleanField(default = False)
    

class GenderCNN(models.Model):
    image = models.CharField(max_length=128)
    pred = models.BooleanField()
    date = models.DateTimeField(default=datetime.now())
    is_delete = models.BooleanField(default = False)