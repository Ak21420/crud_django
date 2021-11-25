from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from crud_operations.forms import EmployeeForm
from crud_operations.models import Employee, Position

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from .serializers import CrudOperationsSerializer

from rest_framework.decorators import api_view

# Create your views here
def employee_list(request):
    context = {'employee_list': Employee.objects.filter(is_delete = False)}
    return render(request, "employee_register/employee_list.html", context)


def employee_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = EmployeeForm()
        else:
            employee = Employee.objects.get(pk=id)
            form = EmployeeForm(instance=employee)
        return render(request, "employee_register/employee_form.html", {'form': form})
    else:
        if id == 0:
            form = EmployeeForm(request.POST)
        else:
            employee = Employee.objects.get(pk=id)
            form = EmployeeForm(request.POST, instance= employee)
        if form.is_valid():
            form.save()
        return redirect('/employee/list')


def employee_delete(request,id):
    employee = Employee.objects.get(pk=id) # (3,)
    employee.is_delete = True
    # employee.delete()
    # form = EmployeeForm(request.POST, instance= employee)
    # print(form)
    # return HttpResponse(form)
    # if form.is_valid():
    employee.save()

    return redirect('/employee/list')


@api_view(['GET', 'POST'])
def employee_api_list(request):
    if request.method == 'GET':
        data = Employee.objects.all()
        

        fullname = request.GET.get('fullname', None)
        if fullname is not None:
            data = data.filter(fullname=fullname)

        id = request.GET.get('id', None)
        if id is not None:
            data = data.filter(id=id)

        Position = request.GET.get('Position', None)
        if Position is not None:
            data = data.filter(position=Position)

        delete = request.GET.get('delete', None)
        if delete is not None:
            if str(delete) == 'false' or str(delete) == '0':
                delete = False
            if str(delete) == 'true' or str(delete) == '1':
                delete = True
            
            data = data.filter(is_delete=delete)

        code = request.GET.get('emp_code', None) or request.GET.get('code', None)
        if code is not None:
            data = data.filter(emp_code=code)
        
        mobile = request.GET.get('mobile', None)
        if mobile is not None:
            data = data.filter(mobile=mobile)
        
        crud_operations_serializer = CrudOperationsSerializer(data, many=True)
        return JsonResponse(crud_operations_serializer.data, safe=False)

    elif request.method == 'POST':
        crud_data = JSONParser().parse(request)
        crud_operations_serializer = CrudOperationsSerializer(data = crud_data)
        
        if crud_operations_serializer.is_valid():
            crud_operations_serializer.save()
            return JsonResponse(crud_operations_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(crud_operations_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # final_data = []
        # crud_data = JSONParser().parse(request)

        # for i in crud_data:
        #     crud_operations_serializer = CrudOperationsSerializer(data = i)
            
        #     if crud_operations_serializer.is_valid():
        #         crud_operations_serializer.save()
        #         final_data.append(crud_operations_serializer.data)
        #     else:
        #         return JsonResponse(crud_operations_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # return JsonResponse(final_data, status=status.HTTP_201_CREATED) 

    # GET list of tutorials, POST a new tutorial, DELETE all tutorials
 
@api_view(['GET'])
def employee_api_list_single(request,pk):
    data = Employee.objects.get(pk=pk) 
        
    if request.method == 'GET':  
        crud_operations_serializer = CrudOperationsSerializer(data, many=False)
        return JsonResponse(crud_operations_serializer.data, safe=False)

@api_view(['DELETE'])
def employee_api_delete(request,pk):
    try:
        data = Employee.objects.get(pk=pk) 
        
        if request.method == 'DELETE': 
            data.is_delete = True
            data.save()
            
            return JsonResponse({'message': 'Employee was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
            
    except Employee.DoesNotExist: 
        return JsonResponse({'message': 'The Employee does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 

# @api_view(['GET', 'PUT', 'DELETE'])
@api_view(['PUT'])
def employee_api_update(request, pk):
    try: 
        data = Employee.objects.get(pk=pk) 

        # if request.method == 'GET': 
        #     crud_operations_serializer = CrudOperationsSerializer(data) 
        #     return JsonResponse(crud_operations_serializer.data) 

        if request.method == 'PUT':
            crud_data = JSONParser().parse(request)
            crud_operations_serializer = CrudOperationsSerializer(data, data=crud_data)
            if crud_operations_serializer.is_valid():
                crud_operations_serializer.save()
                return JsonResponse(crud_operations_serializer.data)
            return JsonResponse(crud_operations_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # elif request.method == 'DELETE': 
        #     data.is_delete = True
        #     data.save()
        #     return JsonResponse({'message': 'Employee was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except Employee.DoesNotExist: 
        return JsonResponse({'message': 'The Employee does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
        
# @api_view(['GET'])
# def employee_api_list_published(request):
#     data = Employee.objects.filter(is_delete = True)
        
#     if request.method == 'GET': 
#         crud_operations_serializer = CrudOperationsSerializer(data, many=True)
#         return JsonResponse(crud_operations_serializer.data, safe = False)
