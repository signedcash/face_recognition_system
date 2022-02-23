from django.contrib.auth.models import User
from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)


class Face(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    type = models.CharField(max_length=30)
    img = models.ImageField(upload_to="images/%Y/%m/%d/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)


class Classifier(models.Model):
    recognizer = models.FileField(upload_to="recognizers/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    face = models.ForeignKey(Face, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True)

# Create your models here.
