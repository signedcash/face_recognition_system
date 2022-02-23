from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('logs/', logs, name='logs'),
    path('faces/', faces, name='faces'),
    path('signin/', SingInUser.as_view(), name='signin'),
    path('test/', test, name='test'),
    path('devices/', devices, name='devices'),
    path('logout/', logout_view, name='logout'),
    path('add_face/', add_face, name='add_face'),
    path('add_device/', add_device, name='add_device'),
    path('delete_face/<int:face_id>/', delete_face, name='delete_face'),
    path('delete_device/<int:device_id>/', delete_device, name='delete_device'),
    path('off_device/<int:device_id>/', off_device, name='off_device'),
    path('on_device/<int:device_id>/', on_device, name='on_device'),
]
