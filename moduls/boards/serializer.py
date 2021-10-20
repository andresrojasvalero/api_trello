from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from moduls.boards.models import Board
from rest_framework import serializers

class AuxCreateSerializer(ModelSerializer):

  class Meta:
    model = User
    fields = ('id', 'username' )

class BoardGetSerializer(ModelSerializer):
  owner = serializers.StringRelatedField()
  members = AuxCreateSerializer(read_only=True, many=True)
  favorite = AuxCreateSerializer(read_only=True, many=True)

  class Meta:
    model = Board
    fields = ('id', 'owner','name', 'description', 'visibility', 'favorite', 'members', 'created_at' )

class BoardPostSerializer(ModelSerializer):

  class Meta:
    model = Board
    fields = ('name', 'description', 'visibility' )

  def create(self, validated_data):
    user = self.context['request'].user
    board = Board.objects.create(**validated_data, owner=user)
    board.members.add(user)
    return board