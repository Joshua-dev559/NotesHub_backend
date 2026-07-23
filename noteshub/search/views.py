from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from notes.models import Note
from notes.serializers import NoteSerializer


class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({'notes': []})

        notes = Note.objects.filter(
            user=request.user,
            deleted_at__isnull=True
        ).filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__icontains=query)
        )

        return Response({'notes': NoteSerializer(notes, many=True).data})
