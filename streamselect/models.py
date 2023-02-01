from django.contrib.auth.models import User
from django.db import models


class userbasicinfo(models.Model):
    uid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    added_on = models.DateTimeField(auto_now=True)
    full_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    DOB = models.DateField()
    gender = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    disability=models.CharField(max_length=100)
    school_name_board = models.CharField(max_length=100)
    mobile_num = models.CharField(max_length=12)
    alt_mobile_num = models.CharField(max_length=12)
    photo = models.ImageField(upload_to='User_image', null=True)
