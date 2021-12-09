from django.conf import settings as conf
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from keras_preprocessing import image
from crud_operations.forms import *
from crud_operations.models import *
from django.core.files.storage import default_storage

import os

from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from .serializers import *

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




def save_image(img_path, f):

    if os.path.isfile(img_path) and os.access(img_path, os.R_OK):
        # print('-----------------------------')
        # print('Exists')
        # print('-----------------------------')
        pass
    else:
        file_name_2 = default_storage.save(img_path, f)
        # print('-----------------------------')
        # print(file_name_2)
        file_url = default_storage.url(file_name_2)
        # print(file_url)
        # print('-----------------------------')

def predict_value(img_path):
    model = load_model('model_files/gender.h5') 

    size = 224
    img = load_img(img_path, target_size = (size, size, 3))

    img = img_to_array(img)
    img = img/255.0
    img = img.reshape(1, size, size, 3)

    return final_prediction(model.predict(img)[0][0])

def final_prediction(prob):
    if prob <= 0.5:
        final_pred = False
        print('female', (1-prob))
    else:
        final_pred = True
        print('male', prob)
    return final_pred
                
# Create your views here.
def gender_class_view(request):
  
    if request.method == 'POST':
        # print(request.POST)
        # form = GenderClassForm(request.POST, request.FILES)
        # gender_class = Gender_CNN.
        img_path = os.path.join(conf.MEDIA_ROOT, str(request.FILES['image']))

        save_image(img_path, request.FILES['image'])

        try: 
            final_pred = predict_value(img_path)

            ob, created = Gender_CNN.objects.update_or_create(
                                    image = img_path, pred = final_pred,
                                    defaults = {'image': img_path, 'pred' : final_pred,
                                            'is_delete' : False, 'date' : datetime.now()},
                                )
            # ob = Gender_CNN.objects.create(image = img_path, pred = final_pred)
            
            # gender_images = Gender_CNN.objects.filter(pk=ob.id)
            # print(ob.image, ob.date, ob.pred)
            # print("----------------------------------")
            # print(ob)
            # print(created)
            # print("----------------------------------")
            # return render(request, 'gender_cnn/gender_class.html', {'img_path' : ob.image,
            #                                                     'final_pred' : ob.pred,
            #                                                     'date' : ob.date})
            
            return redirect('gender_view')

        except Exception as e:
            print('------------------------------------------------')
            print(e)
    
    elif request.method == 'GET':
        form = GenderClassForm()

    return render(request, 'gender_cnn/gender_class.html', {'form' : form})
  
  
def success(request):
    return HttpResponse('successfully uploaded')


def gender_class_list(request):
  
    if request.method == 'GET':
  
        gender_images = Gender_CNN.objects.filter(is_delete = False) 
        
        # print(gender_images[1].date)
        try:
            return render(request, 'gender_cnn/gender_view.html',
                        {'gender_data' : gender_images})
        except Exception as e:
            print(e)

def gender_class_delete(request,id):
    gender_data = Gender_CNN.objects.get(pk=id) # (3,)
    gender_data.is_delete = True
   
    gender_data.save()

    return redirect('gender_view')

def gender_class_update(request,id):
    
    gender_data = Gender_CNN.objects.get(pk=id)
    if request.method == 'POST':
        
        # print(request.FILES['image'])
        try:
            if request.FILES['image']:
                img_path = os.path.join(conf.MEDIA_ROOT, str(request.FILES['image']))

                save_image(img_path, request.FILES['image'])

                try: 
                    final_pred = predict_value(img_path)

                    gender_data.image = img_path
                    gender_data.pred = final_pred
                    gender_data.date = datetime.now()

                    # ob, created = Gender_CNN.objects.update_or_create(
                    #                         image = img_path, pred = final_pred,
                    #                         defaults = {'image': img_path, 'pred' : final_pred,
                    #                                 'is_delete' : False, 'date' : datetime.now()},
                    #                     )
                    gender_data.save()
                    
                    return redirect('gender_view')

                except Exception as e:
                    print('------------------------------------------------')
                    print(e)
        except:
            return redirect('gender_view')
            
        
    elif request.method == 'GET':
        return render(request, 'gender_cnn/gender_update_prediction.html', {'form' : gender_data})
    
    # return render(request, "employee_register/employee_form.html", {'form': form})