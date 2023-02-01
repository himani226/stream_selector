import uuid

from django.contrib.auth.models import User
from django.db import models
from .utility.utility import remove_spaces_with_underscore


class UserBasicInfo(models.Model):
    '''def get_user_image_path(self, filename):
        return '''
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    added_on = models.DateTimeField(auto_now=True)
    full_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    school_name_board = models.CharField(max_length=100)
    mobile_num = models.CharField(max_length=12)
    parents_num = models.CharField(max_length=12)

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
            'school_name_board': self.school_name_board,
            'mobile_num': self.mobile_num,
            'phone_num': self.parents_num,
            # 'user_profile_image': UserImage.objects.filter(agent=self).user_image
        }


'''class UserImage(models.Model):

    def get_user_image_path(self, filename):
        return 'profile/'.format(remove_spaces_with_underscore(self.name), filename)

    name = models.ForeignKey(UserBasicInfo, on_delete=models.CASCADE, null=True)
    user_image = models.ImageField(upload_to='user_profile_image', null=True)
    user_image_ext = models.CharField(max_length=20, blank=True)'''


class SectionFirst(models.Model):
    role_model = models.CharField(max_length=100)
    nature = models.CharField(max_length=100)
    com_skills = models.CharField(max_length=100)
    development_course = models.CharField(max_length=100)
    exam_attempts = models.CharField(max_length=100)
    health_issues = models.CharField(max_length=100)
    drugs = models.CharField(max_length=100)
    school_type = models.CharField(max_length=100)
    attendance = models.CharField(max_length=100)
    scholarship = models.CharField(max_length=100)

    def embed(self, mode="view"):
        return {
            'role_model': self.role_model,
            'nature': self.nature,
            'com_skills': self.com_skills,
            'development_course': self.development_course,
            'exam_attempts': self.exam_attempts,
            'health_issues': self.health_issues,
            'drugs': self.drugs,
            'school_type': self.school_type,
            'attendance': self.attendance,
            'scholarship': self.scholarship,
        }


class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    payment_status = models.CharField(max_length=100)
