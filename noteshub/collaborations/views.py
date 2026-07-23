from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Collaboration
from .serializers import CollaborationSerializer


class CollaborationViewSet(viewsets.ModelViewSet):
    serializer_class = CollaborationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Collaboration.objects.filter(note__user=self.request.user)
