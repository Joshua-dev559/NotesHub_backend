from django.db import models
import uuid
from django.conf import settings
from notes.models import Note


class Collaboration(models.Model):
    ROLE_CHOICES = [
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='collaborations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='collaborations')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'collaborations'
        unique_together = ('note', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} — {self.note} ({self.role})"
