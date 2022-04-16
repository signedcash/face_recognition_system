from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db import models
from rest_framework import generics
from django.views.generic import ListView
from rest_framework.permissions import IsAuthenticated
import json
from sfr.forms import SignInUserForm, AddFaceForm, AddDeviceForm, TestForm
from sfr.models import Face, Device, Log, FaceRec, ImageFace
from sfr.serializers import FaceRecSerializer
from sfr.utils import overfitting_rec, test_rec
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

menu = ["Журнал", "Устройства", "Лица", "Настройки"]


def index(request):
    return redirect('logs', permanent=True)


def logs(request):
    if request.user.is_authenticated:
        log_list = Log.objects.filter(user=request.user).order_by('-time_create')
        return render(request, 'sfr/logs.html', {'title': 'Журнал активности',
                                                 'menu': menu,
                                                 'current_page': 'Журнал',
                                                 'logs': log_list})
    else:
        return redirect('signin')


def devices(request):
    if request.user.is_authenticated:
        devices_list = Device.objects.filter(user=request.user)
        return render(request, 'sfr/devices.html', {'title': 'Список устройств',
                                                    'menu': menu,
                                                    'current_page': 'Устройства',
                                                    'devices_list': devices_list})
    else:
        return redirect('signin')


class FaceRecViewSet(generics.ListAPIView):
    queryset = FaceRec.objects.all()
    serializer_class = FaceRecSerializer

    def get(self, request, *args, **kwargs):
        file = request.data.get('img')
        device_id = request.data.get('device')
        code_device = request.data.get('code')
        device = Device.objects.get(pk=device_id)

        if device.code == code_device:
            user = device.user
            face = FaceRec.objects.create(img=file, device=device)
            pred_face = test_rec(user, face)
            if pred_face:
                print(pred_face.name)
                log = Log.objects.create(device=device, user=device.user, face=pred_face)
                print(log)
                return HttpResponse(json.dumps({'result': 1}), status=200)
        return HttpResponse(json.dumps({'result': 0}), status=200)


def test(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TestForm(request.POST, request.FILES)
            if form.is_valid():
                form.cleaned_data['user'] = request.user
                form.cleaned_data['name'] = 'test'
                form.cleaned_data['type'] = 'test'
                face = Face.objects.create(**form.cleaned_data)
                res = test_rec(request.user, face)
                face.delete()
                print(res)
                return render(request, 'sfr/test.html', {'title': 'Тест',
                                                         'menu': menu,
                                                         'current_page': 'Тест',
                                                         'form': form,
                                                         'result': res})
        else:
            form = TestForm()
        return render(request, 'sfr/test.html', {'title': 'Тест',
                                                 'menu': menu,
                                                 'current_page': 'Тест',
                                                 'form': form,
                                                 'result': ''})
    else:
        return redirect('signin')


def add_face(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddFaceForm(request.POST, request.FILES, user=request.user)
            if form.is_valid():
                form.cleaned_data['user'] = request.user

                face = Face.objects.create(**form.cleaned_data)
                for img in request.FILES.getlist('img'):
                    form.cleaned_data['img'] = img
                    ImageFace.objects.create(img=img, face=face, user=request.user)
                overfitting_rec(request.user)
                return redirect('faces')
        else:
            form = AddFaceForm(user=request.user)
        return render(request, 'sfr/add_face.html', {'title': 'Добавление лица',
                                                     'menu': menu,
                                                     'current_page': 'База лиц',
                                                     'form': form})
    else:
        return redirect('signin')


def add_device(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddDeviceForm(request.POST)
            if form.is_valid():
                form.cleaned_data['user'] = request.user
                Device.objects.create(**form.cleaned_data)
                return redirect('devices')
        else:
            form = AddDeviceForm()
        return render(request, 'sfr/add_device.html', {'title': 'Добавление устройства',
                                                       'menu': menu,
                                                       'current_page': 'Устройства',
                                                       'form': form})
    else:
        return redirect('signin')


def faces(request):
    if request.user.is_authenticated:
        faces_list = Face.objects.filter(user=request.user)
        return render(request, 'sfr/faces.html', {'title': 'База лиц',
                                                  'menu': menu,
                                                  'current_page': 'База лиц',
                                                  'faces_list': faces_list})
    else:
        return redirect('signin')


class SingInUser(LoginView):
    form_class = SignInUserForm
    template_name = 'sfr/signin.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {'title': 'Вход в систему',
                 'current_page': 'Авторизация'}
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('index')


def logout_view(request):
    logout(request)
    return redirect('signin')


def delete_face(request, face_id):
    del_data = Face.objects.get(pk=face_id)
    if del_data.user == request.user:
        del_data.delete()
    overfitting_rec(request.user)
    return redirect('faces')


def delete_device(request, device_id):
    del_data = Device.objects.get(pk=device_id)
    if del_data.user == request.user:
        del_data.delete()
    return redirect('devices')


def off_device(request, device_id):
    del_data = Device.objects.get(pk=device_id)
    if del_data.user == request.user:
        del_data.status = False
        del_data.save()
    return redirect('devices')


def on_device(request, device_id):
    del_data = Device.objects.get(pk=device_id)
    if del_data.user == request.user:
        del_data.status = True
        del_data.save()
    return redirect('devices')

# Create your views here.
