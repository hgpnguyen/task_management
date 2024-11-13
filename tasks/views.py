from django.http import Http404
from .serializers import TaskSerializer, TaskViewSerializer
from .models import Task


from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


class TaskListView(APIView):

    def validate_status(self, status: str):
        status = status.lower().strip()
        if status in ['p', 'c', 'pending', 'completed']:
            return status[0].upper()
        return ''

    def get(self, request):
        status = self.validate_status(request.query_params.get('status', ''))
        if status:
            tasks = Task.objects.filter(status=status)
        else:
            tasks = Task.objects.all()
        return get_paginated_queryset_response(tasks, request)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskViewSerializer(task).data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    
    def get_object(self, task_id: int):
        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise Http404
    
    def get(self, request, task_id: int):
        task = self.get_object(task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def put(self, request, task_id: int):
        task = self.get_object(task_id)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            updatedTask = serializer.save()
            print(updatedTask)
            return Response(TaskViewSerializer(updatedTask).data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, task_id: int):
        task = self.get_object(task_id)
        task.delete()
        return Response({"message": "Task removed."}, status.HTTP_204_NO_CONTENT)


def get_paginated_queryset_response(qs, request):
    paginator = PageNumberPagination()
    page_size = request.query_params.get('page_size', None)
    paginator.page_size = 10
    if page_size:
        try :
            paginator.page_size = int(page_size)
        except:
            pass
    paginator_qs = paginator.paginate_queryset(qs, request)
    serializer = TaskViewSerializer(paginator_qs, many=True)
    return paginator.get_paginated_response(serializer.data)

# Create your views here.
@api_view(["POST"])
def task_create_view(request, *args, **kwargs):
    data = request.data
    serializer = TaskSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def task_get_list_view(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status.HTTP_200_OK)