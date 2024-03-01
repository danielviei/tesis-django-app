from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author_id.email")
    publication = serializers.ReadOnlyField(source="publication_id.id")

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["image"] = instance.author_id.img.url
        return data

    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "author",
            "publication",
            "creation_date",
        ]
