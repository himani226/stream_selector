from django.contrib.auth.models import User
from django.db import models
from .utility.utility import remove_spaces_with_underscore


class UserBasicInfo(models.Model):

    def get_user_image_path(self, filename):
        return ''


    uid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    added_on = models.DateTimeField(auto_now=True)
    full_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    disability=models.CharField(max_length=100)
    school_name_board = models.CharField(max_length=100)
    mobile_num = models.CharField(max_length=12)
    alt_mobile_num = models.CharField(max_length=12)

    def embed(self, mode="view"):
        return {
            'full_name': self.full_name,
            'father_name': self.father_name,
            'mother_name': self.mother_name,
            'dob': self.dob,
            'gender': self.gender,
            'category': self.category,
            'address': self.address,
            'area': self.area,
            'disability': self.disability,
            'school_name_board': self.school_name_board,
            'mobile_num': self.mobile_num,
            'alt_mobile_num': self.alt_mobile_num,
            'user_image': UserImage.objects.filter(agent=self).user_image
        }

class UserImage(models.Model):

    def get_user_image_path(self, filename):
        return 'profile_{0}/name/{1}'.format(remove_spaces_with_underscore(self.name), filename)

    name = models.ForeignKey(UserBasicInfo, on_delete=models.CASCADE, null=True)
    user_image = models.ImageField(upload_to=get_user_image_path, null=True)
    user_image_ext = models.CharField(max_length=20, blank=True)

