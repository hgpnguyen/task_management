from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    status = serializers.CharField(max_length=10)
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']
    
    def validate_status(self, value):
        value = value.lower().strip()
        if value not in ['p', 'c', 'pending', 'completed']:
            raise serializers.ValidationError('This is not a valid value for status')
        return value[0].upper()
    
    
class TaskViewSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']