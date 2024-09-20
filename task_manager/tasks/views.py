"""
TaskViewSet below should be replaced with this one:

        class TaskModelViewSet(ModelViewSet):
            serializer_class = TaskSerializer
            queryset = Task.objects.all()
"""
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)
from rest_framework.viewsets import (
    ModelViewSet,
    ViewSet,
)

from .models.task import Task
from .serializers import TaskSerializer


class TaskViewSet(ViewSet):
    serializer_class = TaskSerializer

    def list(self, request: Request) -> Response:
        serializer = self.serializer_class(
            Task.objects.all().order_by('created'),
            many=True,
        )
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=HTTP_201_CREATED,
        )

    def retrieve(self, request: Request, pk=None) -> Response:
        obj = get_object_or_404(
            Task.objects.all(),
            pk=pk,
        )
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def update(self, request: Request, pk=None) -> Response:
        obj = get_object_or_404(
            Task.objects.all(),
            pk=pk,
        )
        serializer = self.serializer_class(
            obj,
            data=request.data,
            partial=hasattr(request, 'partial'),
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request: Request, pk=None) -> Response:
        request.partial = True
        return self.update(request=request, pk=pk)

    def destroy(self, request: Request, pk=None) -> Response:
        obj = get_object_or_404(
            Task.objects.all(),
            pk=pk,
        )
        obj.delete()
        return Response(status=HTTP_204_NO_CONTENT)
