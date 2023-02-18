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
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pin = models.IntegerField()
    area = models.CharField(max_length=100)
    board = models.CharField(max_length=100)
    school_name = models.CharField(max_length=100)
    school_type = models.CharField(max_length=100)
    mobile_num = models.CharField(max_length=12)
    parents_num = models.CharField(max_length=12)
    check_alerts = models.CharField(max_length=12)

    def embed(self, mode="view"):
        return {
            'full_name': self.full_name,
            'father_name': self.father_name,
            'mother_name': self.mother_name,
            'dob': self.dob,
            'gender': self.gender,
            'category': self.category,
            'address': self.address,
            'district': self.district,
            'state': self.state,
            'city': self.city,
            'pin': self.pin,
            'area': self.area,
            'board': self.board,
            'school_name': self.school_name,
            'school_type': self.school_type,
            'mobile_num': self.mobile_num,
            'phone_num': self.parents_num,
            'check_alerts': self.check_alerts,
            # 'user_profile_image': UserImage.objects.filter(agent=self).user_image
        }


'''class UserImage(models.Model):

    def get_user_image_path(self, filename):
        return 'profile/'.format(remove_spaces_with_underscore(self.name), filename)

    name = models.ForeignKey(UserBasicInfo, on_delete=models.CASCADE, null=True)
    user_image = models.ImageField(upload_to='user_profile_image', null=True)
    user_image_ext = models.CharField(max_length=20, blank=True)'''


class SectionFirst(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    nineth_marks = models.CharField(max_length=100)
    nineth_marks_math = models.CharField(max_length=100)
    nineth_marks_science = models.CharField(max_length=100)
    tenth_marks = models.CharField(max_length=100)
    tenth_marks_math = models.CharField(max_length=100)
    tenth_marks_science = models.CharField(max_length=100)
    math_olampaid = models.CharField(max_length=100)
    sci_olampaid = models.CharField(max_length=100)
    workshop = models.CharField(max_length=100)
    most_preferred_sub = models.CharField(max_length=100)
    least_preferred_sub = models.CharField(max_length=100)


class SectionSecond(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    study_method = models.CharField(max_length=100)
    study_environment = models.CharField(max_length=100)
    study_time_spent = models.CharField(max_length=100)
    games_time = models.CharField(max_length=100)
    screen_time = models.CharField(max_length=100)
    role_model = models.CharField(max_length=100)
    attempts = models.CharField(max_length=100)
    attendance = models.CharField(max_length=100)
    scholarship = models.CharField(max_length=100)
    edu_gap = models.CharField(max_length=100)
    most_preferred_stream = models.CharField(max_length=100)
    least_preferred_stream = models.CharField(max_length=100)



class SectionThree(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    math = models.CharField(max_length=100)
    physics = models.CharField(max_length=100)
    chemistry = models.CharField(max_length=100)
    biology = models.CharField(max_length=100)
    history = models.CharField(max_length=100)
    geography = models.CharField(max_length=100)
    commerce = models.CharField(max_length=100)
    accounts = models.CharField(max_length=100)
    statistics = models.CharField(max_length=100)
    language = models.CharField(max_length=100)


class SectionFour(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    political_science = models.CharField(max_length=100)
    home_science = models.CharField(max_length=100)
    environment_science = models.CharField(max_length=100)
    physical_edu = models.CharField(max_length=100)
    computers = models.CharField(max_length=100)
    typewriting = models.CharField(max_length=100)
    stenography = models.CharField(max_length=100)
    beautician = models.CharField(max_length=100)
    library_asst = models.CharField(max_length=100)
    secretarial_roles = models.CharField(max_length=100)


class SectionFive(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    curricular = models.CharField(max_length=100)
    performance_level = models.CharField(max_length=100)
    father_qual = models.CharField(max_length=100)
    mother_qual = models.CharField(max_length=100)
    sibling_qual = models.CharField(max_length=100)
    father_job = models.CharField(max_length=100)
    mother_job = models.CharField(max_length=100)
    sibling_job = models.CharField(max_length=100)
    mother_preferred_stream = models.CharField(max_length=100)
    father_preferred_stream = models.CharField(max_length=100)
    annual_income = models.CharField(max_length=100)


class SectionSix(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    no_information = models.CharField(max_length=100)
    decision = models.CharField(max_length=100)
    attitude_towards_life = models.CharField(max_length=100)
    problem_solver = models.CharField(max_length=100)
    society_problem = models.CharField(max_length=100)
    monthly_budget = models.CharField(max_length=100)
    own_business = models.CharField(max_length=100)


class SectionSeven(models.Model):
    research_new_medicine = models.CharField(max_length=100)
    reduce_pollution = models.CharField(max_length=100)
    drawing = models.CharField(max_length=100)
    council_people = models.CharField(max_length=100)
    calculation_on_comp = models.CharField(max_length=100)
    yoga_fitness = models.CharField(max_length=100)
    record_temp_bp = models.CharField(max_length=100)
    research_new_things = models.CharField(max_length=100)
    washing_machine_works = models.CharField(max_length=100)
    grocery_record = models.CharField(max_length=100)
    movies_reviews = models.CharField(max_length=100)
    explore_things = models.CharField(max_length=100)


class SectionEight(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    complete_task = models.CharField(max_length=100)
    challenge_books = models.CharField(max_length=100)
    find_new_medicine = models.CharField(max_length=100)
    history_world = models.CharField(max_length=100)
    AI_help = models.CharField(max_length=100)
    logical_thinker = models.CharField(max_length=100)
    manage_finance = models.CharField(max_length=100)
    grp_leader = models.CharField(max_length=100)
    more_practical = models.CharField(max_length=100)
    share_knowledge = models.CharField(max_length=100)
    low_understanding = models.CharField(max_length=100)
    app_development = models.CharField(max_length=100)


class SectionNine(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pollution_reduce = models.CharField(max_length=100)
    imp_fitness = models.CharField(max_length=100)
    leading_nation = models.CharField(max_length=100)
    calculate_analyze = models.CharField(max_length=100)
    curable_medicine = models.CharField(max_length=100)
    machine_human = models.CharField(max_length=100)
    chemicals_change = models.CharField(max_length=100)
    human_creature = models.CharField(max_length=100)


class SectionTen(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    math_difficult = models.CharField(max_length=100)
    science_easy = models.CharField(max_length=100)
    become_actor = models.CharField(max_length=100)
    do_business = models.CharField(max_length=100)
    govt_job = models.CharField(max_length=100)
    become_CA = models.CharField(max_length=100)
    banking_job = models.CharField(max_length=100)
    ilets = models.CharField(max_length=100)
    politics = models.CharField(max_length=100)
    engineering = models.CharField(max_length=100)
    doctor = models.CharField(max_length=100)
    defence = models.CharField(max_length=100)
    farming = models.CharField(max_length=100)
    musician = models.CharField(max_length=100)
    wildlife_expert = models.CharField(max_length=100)
    news_anchor = models.CharField(max_length=100)
    photographer = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    choreographer = models.CharField(max_length=100)
    chef = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    result = models.CharField(max_length=100)

class PaymentCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
