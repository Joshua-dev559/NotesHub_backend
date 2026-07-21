from rest_framework import serializers
from .models import Note
from categories.serializers import CategorySerializer


class NoteSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.UUIDField(
        write_only=True,
        required=False
    )

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "content",
            "category",
            "category_id",
            "is_pinned",
            "is_archived",
            "color",
            "tags",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_at",
            "updated_at",
        ]