from django.db import models

from .base import (
    TimeStampedModel,
    UUIDMixin,
)


class Task(TimeStampedModel, UUIDMixin):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self) -> str:
        return f'{self.title}'
