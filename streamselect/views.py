import re
from django.views.generic.base import View
# import wkhtmltopdf
# from wkhtmltopdf.views import PDFTemplateResponse
import razorpay as razorpay
import six
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.forms import forms
from django.http import HttpResponse, HttpResponseBadRequest, request
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db.models.query_utils import Q
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from stream_selector import settings
from .forms import ProfileForm, SetPasswordForm
from .models import UserBasicInfo, PaymentCheck, SectionFirst, SectionSecond, SectionThree, SectionFour, SectionFive, \
    TestResult
from django.utils.datastructures import MultiValueDictKeyError

# from django_xhtml2pdf.utils import pdf_decorator
SpecialSym =['$', '@', '#', '%']


@csrf_exempt
@login_required(login_url='login/')
def result(request):
    if request.user.is_authenticated:
        user = request.user
        userdetail = UserBasicInfo.objects.get(user_id=user.id)
        first = SectionFirst.objects.get(user_id=user.id)
        second = SectionSecond.objects.get(user_id=user.id)
        third = SectionThree.objects.get(user_id=user.id)
        four = SectionFour.objects.get(user_id=user.id)
        five = SectionFive.objects.get(user_id=user.id)

        context = {'user_detail': userdetail,
                     'first': first,
                     'second': second,
                     'third': third,
                     'four':four,
                     'five':five
                     }
        return render(request, 'result.html', context )


@csrf_exempt
@login_required(login_url='login/')
def home(request):
    if request.user.is_authenticated:
        users = UserBasicInfo.objects.all().count()
        candidate = SectionFive.objects.all().count()
        payment = PaymentCheck.objects.all().count()
        return render(request, 'home.html', {'users': users,
                                             'candidate': candidate,
                                             'payment': payment
                                             })


def index(request):
    return render(request, "index.html")

@csrf_exempt
def register(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) < 5:
            messages.error(request, " Username should more than 5 characters")
            return redirect('register')

        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('register')

        if not any(char.isdigit() for char in pass1):
            messages.error(request, "Password Must contain one number")
            return redirect('register')

        if not any(char.isupper() for char in pass1):
            messages.error(request, "Password Must contain atleast one Capital letter")
            return redirect('register')

        if not any(char.islower() for char in pass1):
            messages.error(request, "Password Must contain atleast one Small letter")
            return redirect('register')

        if not any(char in SpecialSym for char in pass1):
            messages.error(request, "Password Must contain atleast one Special Character '$', '@', '#', '%'")
            return redirect('register')


        if username == "" and pass1 == "" and email == "" and fname == "" and lname == "":
            messages.error(request, "Kindly fill the fields")
            return redirect("register")

        # Create the user
        if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request, " Your account has been successfully created")
            return redirect('login')
        else:
            messages.error(request, "Looks like a username with that email or password already exist")
            return redirect('register')
    else:
        return render(request, 'register.html')

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == "" and password == "":
            messages.error(request, "Kindly fill the fields")
            return redirect("login")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("login")
    else:
        return render(request, 'login.html')


@csrf_exempt
@login_required(login_url='login/')
def profile(request):
    user = request.user
    if not (UserBasicInfo.objects.filter(user_id=user.id).exists()):
        if request.method == 'POST':
            if request.user.is_authenticated:
                name = request.POST['sname']
                fathername = request.POST['fathername']
                mothername = request.POST['mothername']
                dob = request.POST['dob']
                gender = request.POST['gender']
                category = request.POST['category']
                address = request.POST['address']
                state = request.POST['state']
                district = request.POST['district']
                city = request.POST['city']
                pin = request.POST['pin']
                area = request.POST['area']
                board = request.POST['board']
                school = request.POST['school']
                school_type = request.POST['school_type']
                mobile = request.POST['number']
                anumber = request.POST['anumber']
                # photo = request.FILES['image']
                if (name == "" and fathername == "" and mothername == "" and dob == "" and gender == "" and category == "" and \
                        school_type == "" and state == "" and city == "" and district == "" and pin == "" and area == "" and board == "" and school == "" and mobile == "" and anumber == ""):
                    messages.error(request, "Kindly fill the fields")
                    return redirect("profile")

                if (mobile == anumber):
                    messages.error(request, " Both numbers should be different")
                    return redirect('profile')

                if (UserBasicInfo.objects.filter(mobile_num=mobile).exists()):
                    messages.error(request, "Looks like a Mobile Number is already exist")
                    return redirect('profile')

                user = request.user
                profilemodel = UserBasicInfo()
                profilemodel.full_name = name
                profilemodel.father_name = fathername
                profilemodel.mother_name = mothername
                profilemodel.dob = datetime.strptime(dob, "%Y-%m-%d")
                profilemodel.gender = gender
                profilemodel.category = category
                profilemodel.address = address
                profilemodel.state = state
                profilemodel.district = district
                profilemodel.city = city
                profilemodel.pin = pin
                profilemodel.area = area
                profilemodel.board = board
                profilemodel.school_name = school
                profilemodel.school_type = school_type
                profilemodel.mobile_num = mobile
                profilemodel.parents_num = anumber
                profilemodel.user_id = user.id
                profilemodel.check_alerts = "yes"
                profilemodel.save()

                # profilemodel = UserBasicInfo.objects.filter(full_name=name).first()
                # userimage = UserImage()
                # userimage.name = profilemodel
                # userimage.user_image = photo
                # userimage.user_image_ext = photo.name.split('.')[-1]
                # userimage.save()
                messages.success(request, f'Your profile data has been added. Now you can take Stream Selection test')
                return redirect('section_first')
            else:
                messages.error(request, f'Some errors in the form')
                return redirect('profile')
        return render(request, 'profile.html')
    else:
        user = request.user
        userdetail = UserBasicInfo.objects.get(user_id=user.id)
        return render(request, 'profile.html', {'user_detail': userdetail} )


@csrf_exempt
@login_required(login_url='login/')
def section_first(request):
    user = request.user
    try:
        uid = UserBasicInfo.objects.get(user_id=user.id)
        if not SectionFirst.objects.filter(user_id=user.id).exists():
            if request.method == 'POST':
                try:
                    nineth_marks = request.POST['nineth_marks']
                    math_nineth_marks = request.POST['math_nineth_marks']
                    sci_nineth_marks = request.POST['sci_nineth_marks']
                    tenth_marks = request.POST['tenth_marks']
                    math_tenth_marks = request.POST['math_tenth_marks']
                    sci_tenth_marks = request.POST['sci_tenth_marks']
                    math_olympiad = request.POST['math_olympiad']
                    sci_olympiad = request.POST['sci_olympiad']
                    sci_workshop = request.POST['workshop']
                    most_preferred_sub = request.POST['most_preferred_sub']
                    least_preferred_sub = request.POST['least_preferred_sub']

                    if nineth_marks == "" and math_nineth_marks == "" and sci_nineth_marks == "" and tenth_marks == "" and math_tenth_marks == "" and sci_tenth_marks == "" and \
                            math_olympiad == "" and sci_olympiad == "" and sci_workshop == "" and most_preferred_sub == "" and least_preferred_sub == "":
                        messages.error(request, "Kindly fill the fields")
                        return redirect("section_first")
                    if request.user.is_authenticated:
                        firstmodel = SectionFirst()
                        firstmodel.nineth_marks = nineth_marks
                        firstmodel.nineth_marks_math = math_nineth_marks
                        firstmodel.nineth_marks_science = sci_nineth_marks
                        firstmodel.tenth_marks = tenth_marks
                        firstmodel.tenth_marks_math = math_tenth_marks
                        firstmodel.tenth_marks_science = sci_tenth_marks
                        firstmodel.math_olampaid = math_olympiad
                        firstmodel.sci_olampaid = sci_olympiad
                        firstmodel.workshop = sci_workshop
                        firstmodel.most_perfered_sub = most_preferred_sub
                        firstmodel.least_perfered_sub = least_preferred_sub
                        firstmodel.user_id = user.id
                        firstmodel.save()

                        # check errors
                        # success message redirect to result page
                        messages.success(request, f'Your data has been added.')
                        return redirect('section_second')
                    else:
                        messages.error(request, f'Some error in the form.')
                        return redirect('section_first')
                except MultiValueDictKeyError:
                    messages.success(request, f'Already filled the previous section.')
                    return redirect('section_second')
        else:
            messages.error(request, f'Already filled the Section 1.  Kindly fill section 2')
            return redirect('section_second')
    except UserBasicInfo.DoesNotExist:
        messages.error(request, f'You forgot to fill Student Information form. Kindly fill it first.')
        return redirect('profile')

    return render(request, 'section_first.html')

@csrf_exempt
@login_required(login_url='login/')
def section_second(request):
    user = request.user
    try:
        uid = UserBasicInfo.objects.get(user_id=user.id)
        if not SectionSecond.objects.filter(user_id=user.id).exists():
            if request.method == 'POST':
                try:
                    study_method = request.POST['study_method']
                    study_environment = request.POST['study_environment']
                    study_time_spent = request.POST['time_spent']
                    games_time = request.POST['games_time']
                    screen_time = request.POST['screen_time']
                    role_model = request.POST['role_model']
                    attempts = request.POST['attempts']
                    attendance = request.POST['attendance']
                    scholarship = request.POST['scholarship']
                    edu_gap = request.POST['edu_gap']

                    if study_method == "" and study_environment == "" and study_time_spent == "" and games_time == "" and screen_time == "" and \
                            role_model == "" and attempts == "" and attendance == "" and edu_gap == "" and scholarship == "":
                        messages.error(request, "Kindly fill the fields")
                        return redirect("section_second")
                    if request.user.is_authenticated:
                        secondmodel = SectionSecond()
                        secondmodel.study_method = study_method
                        secondmodel.study_environment = study_environment
                        secondmodel.study_time_spent = study_time_spent
                        secondmodel.games_time = games_time
                        secondmodel.screen_time = screen_time
                        secondmodel.role_model = role_model
                        secondmodel.attempts = attempts
                        secondmodel.attendance = attendance
                        secondmodel.scholarship = scholarship
                        secondmodel.edu_gap = edu_gap
                        secondmodel.user_id = user.id
                        secondmodel.save()

                        # check errors
                        # success message redirect to result page
                        messages.success(request, f'Your data has been added.')
                        return redirect('section_three')
                    else:
                        messages.error(request, f'Some error in the form.')
                        return redirect('section_second')
                except MultiValueDictKeyError:
                    messages.success(request, f'Already filled the previous section.')
                    return redirect('section_three')
        else:
            messages.error(request, f'Already filled the Section 2.  Kindly fill section 3')
            return redirect('section_three')
    except UserBasicInfo.DoesNotExist:
        messages.error(request, f'You forgot to fill Student Information form. Kindly fill it first.')
        return redirect('profile')
    return render(request, 'section_second.html')

@csrf_exempt
@login_required(login_url='login/')
def section_three(request):
    user = request.user
    try:
        uid = UserBasicInfo.objects.get(user_id=user.id)
        if not SectionThree.objects.filter(user_id=user.id).exists():
            if request.method == 'POST':
                try:
                    math = request.POST['math']
                    physics = request.POST['physics']
                    chemistry = request.POST['chemistry']
                    biology = request.POST['biology']
                    history = request.POST['history']
                    geography = request.POST['geography']
                    commerce = request.POST['commerce']
                    accounts = request.POST['accounts']
                    statistics = request.POST['statistics']
                    language = request.POST['language']

                    if math == "" and history == "" and biology == "" and chemistry == "" and physics == "" and \
                            statistics == "" and accounts == "" and commerce == "" and geography == "" and language == "":
                        messages.error(request, "Kindly fill the fields")
                        return redirect("section_three")
                    if request.user.is_authenticated:
                        thirdmodel = SectionThree()
                        thirdmodel.math = math
                        thirdmodel.history = history
                        thirdmodel.biology = biology
                        thirdmodel.physics = physics
                        thirdmodel.chemistry = chemistry
                        thirdmodel.geography = geography
                        thirdmodel.commerce = commerce
                        thirdmodel.accounts = accounts
                        thirdmodel.statistics = statistics
                        thirdmodel.language = language
                        thirdmodel.user_id = user.id
                        thirdmodel.save()

                        # check errors
                        # success message redirect to result page
                        messages.success(request, f'Your data has been added.')
                        return redirect('section_four')
                    else:
                        messages.error(request, f'Some error in the form.')
                        return redirect('section_three')
                except MultiValueDictKeyError:
                    messages.success(request, f'Already filled the previous section.')
                    return redirect('section_four')
        else:
            messages.error(request, f'Already filled the Section 3.  Kindly fill section 4')
            return redirect('section_four')
    except UserBasicInfo.DoesNotExist:
        messages.error(request, f'You forgot to fill Student Information form. Kindly fill it first.')
        return redirect('profile')

    return render(request, 'section_three.html')

@csrf_exempt
@login_required(login_url='login/')
def section_four(request):
    user = request.user
    try:
        uid = UserBasicInfo.objects.get(user_id=user.id)
        if not SectionFour.objects.filter(user_id=user.id).exists():
            if request.method == 'POST':
                try:
                    political_science = request.POST['political_science']
                    home_science = request.POST['home_science']
                    environment_science = request.POST['environment_science']
                    physical_edu = request.POST['physical_edu']
                    computers = request.POST['computer']
                    typewriting = request.POST['typewriting']
                    stenography = request.POST['stenography']
                    beautician = request.POST['beautician']
                    library_asst = request.POST['library_asst']
                    secretarial_roles = request.POST['secretarial_roles']
                    if political_science == "" and home_science == "" and environment_science == "" and physical_edu == "" and computers == "" and \
                            typewriting == "" and stenography == "" and beautician == "" and library_asst == "" and secretarial_roles == "":
                        messages.error(request, "Kindly fill the fields")
                        return redirect("section_four")
                    if request.user.is_authenticated:
                        fourthmodel = SectionFour()
                        fourthmodel.political_science = political_science
                        fourthmodel.home_science = home_science
                        fourthmodel.environment_science = environment_science
                        fourthmodel.physical_edu = physical_edu
                        fourthmodel.computers = computers
                        fourthmodel.typewriting = typewriting
                        fourthmodel.stenography = stenography
                        fourthmodel.beautician = beautician
                        fourthmodel.library_asst = library_asst
                        fourthmodel.secretarial_roles = secretarial_roles
                        fourthmodel.user_id = user.id
                        fourthmodel.save()

                        # check errors
                        # success message redirect to result page
                        messages.success(request, f'Proceed with next section 5.')
                        return redirect('section_five')
                    else:
                        messages.error(request, f'Some Errors')
                        return redirect('section_four')
                except MultiValueDictKeyError:
                    messages.success(request, f'Already filled the previous section.')
                    return redirect('section_five')
        else:
            messages.error(request, f'Already filled the Section 4.  Kindly fill section 5')
            return redirect('section_five')
    except UserBasicInfo.DoesNotExist:
        messages.error(request, f'You forgot to fill Student Information form. Kindly fill it first.')
        return redirect('profile')
    return render(request, 'section_four.html')

@csrf_exempt
@login_required(login_url='login/')
def section_five(request):
    user = request.user
    try:
        uid = UserBasicInfo.objects.get(user_id=user.id)
        if not SectionFive.objects.filter(user_id=user.id).exists():
            if request.method == 'POST':
                try:
                    curricular = request.POST['curricular']
                    performance_level = request.POST['performance_level']
                    father_qual = request.POST['father_qual']
                    mother_qual = request.POST['mother_qual']
                    sibling_qual = request.POST['sibling_qual']
                    father_job = request.POST['father_job']
                    mother_job = request.POST['mother_job']
                    sibling_job = request.POST['sibling_job']
                    annual_income = request.POST['annual_income']

                    if curricular == "" and performance_level == "" and father_qual == "" and mother_qual == "" and \
                            sibling_qual == "" and father_job == "" and mother_job == "" and sibling_job == "" and annual_income == "":
                        messages.error(request, "Kindly fill the fields")
                        return redirect("section_five")
                    if request.user.is_authenticated:
                        fifthmodel = SectionFive()
                        fifthmodel.curricular = curricular
                        fifthmodel.performance_level = performance_level
                        fifthmodel.father_qual = father_qual
                        fifthmodel.mother_qual = mother_qual
                        fifthmodel.sibling_qual = sibling_qual
                        fifthmodel.father_job = father_job
                        fifthmodel.mother_job = mother_job
                        fifthmodel.sibling_job = sibling_job
                        fifthmodel.annual_income = annual_income
                        fifthmodel.user_id = user.id
                        fifthmodel.save()

                        # check errors
                        # success message redirect to result page
                        messages.success(request,f'You had given your test successfully. Now you can proceed with payment for result')
                        return redirect('result')
                    else:
                        messages.error(request, f'Some error in the form.')
                        return redirect('section_five')
                except MultiValueDictKeyError:
                    messages.success(request, f'You had given your test successfully. Now you can proceed with payment for result')
                    return redirect('result')
        else:
            messages.error(request, f'answer Already given the test. Kindly check result')
            return redirect('result')
    except UserBasicInfo.DoesNotExist:
        messages.error(request, f'You forgot to fill Student Information form. Kindly fill it first.')
        return redirect('profile')

    return render(request, 'section_five.html')


def section_six(request):
    return render(request, 'section_six.html')


def section_seven(request):
    return render(request, 'section_seven.html')


def section_eight(request):
    return render(request, 'section_eight.html')


def section_nine(request):
    return render(request, 'section_nine.html')


def section_ten(request):
    return render(request, 'section_ten.html')

@csrf_exempt
@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'password_reset_confirm.html', {'form': form})


class ActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.username)


account_activation_token = ActivationTokenGenerator()

@csrf_exempt
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                                     """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                                     )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('home')

    form = PasswordResetForm()
    return render(request, "password_reset.html", context={"form": form})

@csrf_exempt
def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('homepage')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("home")

@csrf_exempt
@login_required
def checkout(request):
    user = request.user

    currency = 'INR'
    amount = 10000  # Rs. 100

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'payment_handler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request, 'checkout.html', context=context)


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def payment_handler(request):
    # only accept POST request.
    if request.method == "POST":
        user = request.user
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 10000  # Rs. 100
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    check = PaymentCheck()
                    check.user = user.id
                    check.order_id = payment_id
                    payment_status = "Success"
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:

                    # if there is an error while capturing payment.
                    return render(request, 'paymentfailure.html')
            else:

                # if signature verification fails.
                return render(request, 'paymentfailure.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()

@csrf_exempt
def error_404_view(request, exception):
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')
