from django.http import Http404
from .serializers import TaskSerializer, TaskViewSerializer
from .models import Task


from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

# Create your views here.
# API view that allows user to create task or view and filter list of tasks
class TaskListView(APIView):

    # Get pagination response
    def get_paginated_queryset_response(self, qs, request):
        paginator = PageNumberPagination()
        page_size = request.query_params.get('page_size', None)
        paginator.page_size = 10 # Default page size
        if page_size:
            try :
                paginator.page_size = int(page_size)
            except:
                pass
        paginator_qs = paginator.paginate_queryset(qs, request)
        serializer = TaskViewSerializer(paginator_qs, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    # Validate if status parameter in url is in form of ('p', 'c', 'pending', 'completed') or return empty
    def validate_status(self, status: str):
        status = status.lower().strip()
        if status in ['p', 'c', 'pending', 'completed']:
            return status[0].upper()
        return ''

    # Filter task with status and return pagination result
    def get(self, request):
        status = self.validate_status(request.query_params.get('status', ''))
        if status:
            tasks = Task.objects.filter(status=status)
        else:
            tasks = Task.objects.all()
        return self.get_paginated_queryset_response(tasks, request)
    
    # Create new task
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskViewSerializer(task).data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

# API View for view, update, delete a specific task
class TaskDetailView(APIView):
    
    # Get task or return 404
    def get_object(self, task_id: int):
        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise Http404
    
    # View task
    def get(self, request, task_id: int):
        task = self.get_object(task_id)
        serializer = TaskViewSerializer(task)
        return Response(serializer.data, status.HTTP_200_OK)
    
    # Update task
    def put(self, request, task_id: int):
        task = self.get_object(task_id)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            updatedTask = serializer.save()
            return Response(TaskViewSerializer(updatedTask).data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    # Delete task
    def delete(self, request, task_id: int):
        task = self.get_object(task_id)
        task.delete()
        return Response({"message": "Task removed."}, status.HTTP_204_NO_CONTENT)


