from django.db import models
from moduls.lists.models import List
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Card(models.Model):
  owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  name = models.CharField(max_length=150)
  list = models.ForeignKey(List, on_delete=models.CASCADE)
  description = models.CharField(max_length=500)
  members = models.ManyToManyField(User, related_name='cards')
  position = models.IntegerField(
    validators=[
      MaxValueValidator(100),
      MinValueValidator(1)
    ]
  )
  created_at = models.DateTimeField(auto_now_add=True)
  finalization_at = models.DateTimeField(null=True)