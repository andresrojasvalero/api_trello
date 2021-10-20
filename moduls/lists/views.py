from django.db.models import query
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from moduls.lists.models import List
from moduls.lists.serializer import SerializarCreateList, GetSerializerList, AuxSerializerCards
from moduls.lists.permissions import ListPermissions
from rest_framework import status
from rest_framework.decorators import action
# Create your views here.

class ListModelViewSet(ModelViewSet):
  queryset = List.objects.all()
  serializer_class = SerializarCreateList
  permission_classes = [ListPermissions]
  
  def get_queryset(self):
    data={}
    for k, v in self.request.query_params.items():
      data[k] = v
    return self.queryset.filter(**data)
    
  def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    serialized = GetSerializerList(queryset, many=True)
    return Response(status=status.HTTP_200_OK, data=serialized.data)

  @action(methods=['GET'], detail=True)
  def cards(self, request, pk):
    board = request.data.get('board')
    if not board:
      board = request.query_params.get('board')
      if not board:
        return Response(status=status.HTTP_400_BAD_REQUEST)
      board = request.query_params.get('board')[0]

    queryset = self.get_queryset().filter(board=board, id=pk)

    if not queryset.exists():
      return Response(status=status.HTTP_404_NOT_FOUND)
    cards = queryset[0].card_set.all()
    serialized = AuxSerializerCards(cards, many=True)
    return Response(status=status.HTTP_200_OK, data=serialized.data)

  @action(methods=['PUT'], detail=True)
  def order(self, request, pk):
    board = request.data.get('board')
    new_position = request.data.get('order')

    try:
      board = int(board)
      new_position = int(new_position)
    except:
      return Response(status=status.HTTP_400_BAD_REQUEST)

    if new_position < 1:
      return Response(status=status.HTTP_400_BAD_REQUEST)

    queryset = self.get_queryset().filter(board=board)

    if not queryset.exists():
      return Response(status=status.HTTP_404_NOT_FOUND)

    list_data = queryset.filter(id=pk) 
    if not list_data.exists():
      return Response(status=status.HTTP_404_NOT_FOUND)

    old_position = list_data[0].position

    if old_position == new_position:
      return Response(status=status.HTTP_400_BAD_REQUEST)

    if new_position < old_position:
      for list in queryset:
        if list.position < new_position or list.position >= old_position:
          continue
        queryset.filter(id=list.id).update(position=list.position + 1)
      list_data.update(position=new_position)

    if new_position > old_position:
      for list in queryset:
        if list.position <= old_position or list.position > new_position:
          continue
        queryset.filter(id=list.id).update(position=list.position - 1)
      list_data.update(position=new_position)
    return Response(status=status.HTTP_200_OK)
