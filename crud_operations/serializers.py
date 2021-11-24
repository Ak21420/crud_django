from rest_framework import serializers 
from .models import Employee, Position
 
 
class CrudOperationsSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Employee
        fields = ('id',
                  'fullname',
                  'emp_code',
                  'mobile',
                  'position',
                  'is_delete')