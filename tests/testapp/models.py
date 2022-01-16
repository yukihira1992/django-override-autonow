from django.db import models


class AutoFieldsModel(models.Model):
    date_auto_now = models.DateField(auto_now=True, null=True)
    date_auto_now_add = models.DateField(auto_now_add=True, null=True)
    datetime_auto_now = models.DateTimeField(auto_now=True, null=True)
    datetime_auto_now_add = models.DateTimeField(auto_now_add=True, null=True)


class AutoFieldsModel2(models.Model):
    date_auto_now = models.DateField(auto_now=True, null=True)
    date_auto_now_add = models.DateField(auto_now_add=True, null=True)
    datetime_auto_now = models.DateTimeField(auto_now=True, null=True)
    datetime_auto_now_add = models.DateTimeField(auto_now_add=True, null=True)
