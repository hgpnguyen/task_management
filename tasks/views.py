from django.shortcuts import render
from .serializers import TaskSerializer
from .models import Task

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
@api_view(["POST"])
def task_create_view(request, *args, **kwargs):
    data = request.data
    serializer = TaskSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    return Response({}, status.HTTP_400_BAD_REQUEST)


@api_view(["UPDATE"])
def task_update_view(request, task_id, *args, **kwargs):
    try:
        task = Task.objects.get(id=task_id)
    except:
        return Response({}, status.HTTP_404_NOT_FOUND)
    data = request.data
    serializer = TaskSerializer(task, data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE", "POST"])
def task_delete_view(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except:
        return Response({}, status.HTTP_404_NOT_FOUND)
    task.delete()
    return Response({"message": "Task removed."}, status.HTTP_200_OK)
    
@api_view(["GET"])
def task_get_list_view(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status.HTTP_200_OK)