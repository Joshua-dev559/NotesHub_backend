from django.db.models import Q
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Note
from .serializers import NoteSerializer
from .permissions import IsOwnerOrReadOnly


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsOwnerOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "category",
        "is_pinned",
        "is_archived",
        "color",
    ]

    search_fields = [
        "title",
        "content",
        "tags",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "title",
    ]

    def get_queryset(self):
        return Note.objects.filter(
            user=self.request.user,
            deleted_at__isnull=True
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def toggle_pin(self, request, pk=None):
        note = self.get_object()
        note.is_pinned = not note.is_pinned
        note.save()
        return Response({"is_pinned": note.is_pinned})

    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        note = self.get_object()
        note.is_archived = not note.is_archived
        note.save()
        return Response({"is_archived": note.is_archived})

    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.query_params.get("q", "")

        notes = self.get_queryset().filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

        serializer = self.get_serializer(notes, many=True)
        return Response(serializer.data)