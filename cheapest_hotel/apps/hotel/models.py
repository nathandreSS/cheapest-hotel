from django.db import models
from django.core.validators import MinValueValidator


class Hotel(models.Model):
    name = models.CharField('Name', max_length=200, unique=True)
    stars = models.PositiveSmallIntegerField('Stars', validators=[MinValueValidator(1)])
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now=True)

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'
        ordering = ['name', 'stars']

    def __str__(self):
        return self.name


class Tax(models.Model):
    USERS = [
        (1, 'Regular'),
        (2, 'Reward')
    ]
    name = models.CharField('Name', max_length=200)
    price = models.FloatField('Price', validators=[MinValueValidator(0.0)])
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.IntegerField(choices=USERS)
    monday = models.BooleanField('Monday', default=False)
    tuesday = models.BooleanField('Tuesday', default=False)
    wednesday = models.BooleanField('Wednesday', default=False)
    thursday = models.BooleanField('Thursday', default=False)
    friday = models.BooleanField('Friday', default=False)
    saturday = models.BooleanField('Saturday', default=False)
    sunday = models.BooleanField('Sunday', default=False)

    def __str__(self):
        return self.name
