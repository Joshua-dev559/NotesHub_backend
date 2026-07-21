from django.db import models
import uuid
# Create your models here.
from users.models import User
from categories.models import Category


class Note(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notes"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notes"
    )

    title = models.CharField(max_length=255)

    content = models.TextField()

    is_pinned = models.BooleanField(default=False)

    is_archived = models.BooleanField(default=False)

    color = models.CharField(
        max_length=7,
        default="#ffffff"
    )

    tags = models.JSONField(
        default=list,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        db_table = "notes"

        ordering = [
            "-is_pinned",
            "-updated_at",
        ]

        indexes = [
            models.Index(fields=["user", "is_archived"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return self.title