from moduls.comments.serializer import CommentSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from moduls.cards.models import Card

class CardSerializer(ModelSerializer):

    class Meta:
        model = Card
        fields = ('name', 'description', 'members','position', 'created_at', 'list')
