from django.conf.urls import url
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.employee_form,name='employee_insert'), # get and post req. for insert operation
    path('<int:id>/', views.employee_form,name='employee_update'), # get and post req. for update operation
    path('delete/<int:id>/',views.employee_delete,name='employee_delete'),
    path('list/',views.employee_list,name='employee_list'), # get req. to retrieve and display all records

    url(r'^api/api_list$', views.employee_api_list),
    # url(r'^api/api_create$', views.employee_form),
    url(r'^api/api_update/(?P<pk>[0-9]+)$', views.employee_api_update),
    # url(r'^api/create/(?P<pk>[0-9]+)$', views.tutorial_detail),
    url(r'^api/api_list_single/(?P<pk>[0-9]+)$', views.employee_api_list_single),
    url(r'^api/api_delete/(?P<pk>[0-9]+)$', views.employee_api_delete),

    path('gender_prediction', views.gender_class_view, name = 'gender_prediction'),
    path('gender_view', views.gender_class_list, name = 'gender_view'),
    path('success', views.success, name = 'success'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
