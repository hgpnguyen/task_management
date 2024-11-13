from rest_framework import serializers
from .models import Task

# Serializer for create, update, delete
class TaskSerializer(serializers.ModelSerializer):
    status = serializers.CharField(max_length=10)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status']
    
    # Accept status value in form of ('p', 'c', 'pending', 'completed)
    def validate_status(self, value):
        value = value.lower().strip()
        if value not in ['p', 'c', 'pending', 'completed']:
            raise serializers.ValidationError('This is not a valid value for status')
        return value[0].upper()
    
# Serializer for view   
class TaskViewSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display') # Show display name of status
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status']