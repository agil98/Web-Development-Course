from django.db import models

# Create your models here.
SIZE = (
    ('S', 'small'),
    ('L', 'large'),
)

STYLE = (
    ('R', 'regular'),
    ('S', 'sicilian'),
)

class Pizza(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} - {self.price}"

class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return f"{self.name} - {self.price}"

class Sub(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return f"{self.name} - {self.price}"

class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return f"{self.name} - {self.price}"

class DinnerPlatter(models.Model):
    name = models.CharField(max_length=64)
    size = models.CharField(max_length = 64, choices = SIZE, default='small')
    price = models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return f"{self.name} - {self.price}"
    
