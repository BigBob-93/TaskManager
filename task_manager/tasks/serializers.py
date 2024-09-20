from rest_framework.serializers import ModelSerializer

from .models.task import Task


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'completed',
        )
