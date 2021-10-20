from rest_framework.serializers import ModelSerializer
from moduls.comments.models import Comment

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'message', 'created_at', 'card', 'owner')