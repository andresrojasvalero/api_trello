from django.db import models
from django.contrib.auth.models import User
from moduls.cards.models import Card

# Create your models here.

class Comment(models.Model):
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  card = models.ForeignKey(Card, on_delete=models.CASCADE)
  message = models.CharField(max_length=150)
  created_at = models.DateTimeField(auto_now_add=True)
