from rest_framework import serializers
from moduls.lists.models import List
from moduls.cards.models import Card

class SerializarCreateList(serializers.ModelSerializer):

  class Meta:
    model = List
    fields = ('name', 'board', 'position', )

class GetSerializerList(serializers.ModelSerializer):
  
  class Meta:
    model = List
    fields = ('id', 'name', 'board', 'position', )

class AuxSerializerCards(serializers.ModelSerializer):

  owner = serializers.PrimaryKeyRelatedField(read_only=True)
  members = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

  class Meta:
    model = Card
    fields = ('owner', 'name', 'description', 'members', 'position', 'created_at', 'finalization_at' )