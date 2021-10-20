from django.db import models
from django.contrib.auth.models import User

# Create your models here.

VISIVILITY_CHOICES = [
  ('public', 'public'),
  ('private', 'private'),
  ('space_of_work', 'space_of_work'),
] 

class Board(models.Model):
  owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=500)
  visibility = models.CharField(choices=VISIVILITY_CHOICES, max_length=13)
  favorite = models.ManyToManyField(User, related_name='favorites')
  members = models.ManyToManyField(User, related_name='members')
  created_at = models.DateTimeField(auto_now_add=True)