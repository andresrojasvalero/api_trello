from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
#
from moduls.comments.serializer import CommentSerializer
from moduls.cards.serializer import CardSerializer
from moduls.cards.models import Card


class CardViews(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    @action(methods=['GET', 'POST'], detail=True)
    def comments(self, request, pk):
        card = self.get_object()

        if request.method == 'GET':
            serialized = CommentSerializer(card.comments, read_only = True, many=True)
            return Response(
                status = status.HTTP_200_OK,
                data= serialized.data
            )

        if request.method == 'POST':
            comment = request.data
            serializer = CommentSerializer(data=comment)
            if not serializer.is_valid(raise_exception=True):
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)