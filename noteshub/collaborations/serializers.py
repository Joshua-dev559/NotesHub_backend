from rest_framework import serializers
from .models import Collaboration


class CollaborationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaboration
        fields = ['id', 'note', 'user', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']
