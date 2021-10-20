from rest_framework.viewsets import ModelViewSet
from moduls.boards.models import Board
from moduls.boards.serializer import BoardPostSerializer, BoardGetSerializer
from moduls.boards.permissions import BoardPermissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

class BoarsdModelViewSet(ModelViewSet):
  queryset = Board.objects.all()
  serializer_class = BoardPostSerializer
  permission_classes = [ BoardPermissions ]

  def retrieve(self, request, pk=None):
    queryset = self.get_object()
    isUser =  queryset.members.all().filter(id=request.user.id)

    if len(isUser) == 0:
      return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

    serialized = BoardGetSerializer(queryset)

    return Response(status=status.HTTP_200_OK, data=serialized.data)

  def list(self, request, *args, **kwargs):
    queryset = self.get_queryset().filter(members=request.user)
    serialized = BoardGetSerializer(queryset, many=True)
    
    return Response(status=status.HTTP_200_OK, data=serialized.data)

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    headers = self.get_success_headers(serializer.data)
    return Response(data={'id':serializer.instance.id, **serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

  @action(methods=['POST', 'DELETE'], detail=True)
  def members(self, request, pk):
    queryset = self.get_queryset().filter(id=pk)
    id_member = request.data.get('id')
    
    if not id_member:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    if not queryset.exists():
      return Response(status=status.HTTP_404_NOT_FOUND)

    try:
      id_member = int(id_member)
    except:
      return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = BoardGetSerializer(queryset[0])
    member_exist = False

    for isMember in serializer.data['members']:
      if isMember['id'] == id_member:
        member_exist = True
      
    if request.method == 'POST' and serializer.instance.owner_id == request.user.id:
      if id_member == request.user.id or member_exist:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'user alread'})

      queryset[0].members.add(id_member)

      return Response(status=status.HTTP_201_CREATED)
    if request.method == 'DELETE' and member_exist:
      if id_member == serializer.instance.owner_id:
        return Response(status=status.HTTP_400_BAD_REQUEST)

      queryset[0].members.remove(id_member)

      return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)

  @action(methods=['POST', 'DELETE'], detail=True)
  def favorites(self, request, pk):
    queryset = self.get_queryset().filter(id=pk)
    
    if not queryset.exists():
      return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = BoardGetSerializer(queryset[0])
    member_exist = False

    for isMember in serializer.data['members']:
      if isMember['id'] == request.user.id:
        member_exist = True

    if not member_exist:
      return Response(status=status.HTTP_400_BAD_REQUEST)

    is_favorite = False

    for isMember in serializer.data['favorite']:
      if isMember['id'] == request.user.id:
        is_favorite = True

    if request.method == 'POST':
      if is_favorite:
        return Response(status=status.HTTP_400_BAD_REQUEST)

      queryset[0].favorite.add(request.user.id)

      return Response(status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
      if not is_favorite:
        return Response(status=status.HTTP_400_BAD_REQUEST)

      queryset[0].favorite.remove(request.user.id)

      return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)