from moduls.comments.serializer import CommentSerializer
from moduls.comments.models import Comment
from rest_framework.viewsets import ModelViewSet

# Create your views here.
class CommentViews(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer