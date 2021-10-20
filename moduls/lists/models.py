from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from moduls.boards.models import Board

# Create your models here.

class List(models.Model):
  name = models.CharField(max_length=150)
  board = models.ForeignKey(Board, on_delete=models.CASCADE)
  position = models.IntegerField(
    validators=[
      MaxValueValidator(100),
      MinValueValidator(1)
    ]
  )
  created_at = models.DateTimeField(auto_now_add=True)