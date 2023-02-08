import re
from django.views.generic.base import View
#import wkhtmltopdf
#from wkhtmltopdf.views import PDFTemplateResponse
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
from .models import UserBasicInfo,PaymentCheck, SectionFirst, SectionSecond

#from django_xhtml2pdf.utils import pdf_decorator

def result(request):
    if request.user.is_authenticated:
        user=request.user
        userdetail = UserBasicInfo.objects.get(user_id=user.id)
    return render(request, 'result.html',{'user_detail':userdetail})


# Creating a class based view
'''class generate_report(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user=request.user
            userdetail = UserBasicInfo.objects.get(user_id=user.id)
            open('result.html', "w").write(render_to_string('result.html', {'user_detail': userdetail}))

            # Converting the HTML template into a PDF file
            pdf = html_to_pdf('result.html')

            # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')'''

'''@pdf_decorator(pdfname='Psychometric_Test_Result.pdf')
def generate_report(request):
    if request.user.is_authenticated:
        user=request.user
        userdetail = UserBasicInfo.objects.get(user_id=user.id)
    return render(request, 'result.html',{'user_detail':userdetail})'''

'''class MyPDFView(View):
    template = 'result.html'  # the template

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            userdetail = UserBasicInfo.objects.get(user_id=user.id)
        data = {"user_detail": userdetail}  # data that has to be renderd to pdf templete

        response = PDFTemplateResponse(request=request,
                                       template=self.template,
                                       filename="hello.pdf",
                                       context=data,
                                       show_content_in_browser=False,
                                       cmd_options={'margin-top': 10,
                                                    "zoom": 1,
                                                    "viewport-size": "1366 x 513",
                                                    'javascript-delay': 1000,
                                                    'footer-center': '[page]/[topage]',
                                                    "no-stop-slow-scripts": True},
                                       )
        return response'''


@login_required()
def home(request):
    return render(request, 'home.html')


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

        if not username.isalnum():
            messages.error(request, " User name should contain letters and numbers")
            return redirect('register')

        '''if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', pass1):
            messages.error(request,"Password Must contain atleast one letter, one number,one special character. Minimum length should be 8 characters")
            return redirect('register')'''

        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('register')

        if username == "" and pass1 == "" and email == "" and fname == "" and lname == "":
            messages.error(request, "Kindly fill the fields")
            return redirect("register")

        # Create the user
        if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.save()
            messages.success(request, " Your account has been successfully created")
            return redirect('home')
        else:
            messages.error(request, "Looks like a username with that email or password already exist")
            return redirect('register')
        return render(request, 'register.html', context)
    else:
        return render(request, 'register.html')


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

@login_required
def profile(request):
    if request.method == 'POST':
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
        mobile = request.POST['number']
        anumber = request.POST['anumber']
        #photo = request.FILES['image']
        if name == "" and fathername == "" and mothername == "" and dob == "" and gender == "" and category == "" and \
                address == "" and state=="" and city=="" and district =="" and pin=="" and area == "" and board == "" and school == "" and mobile == "" and anumber == "":
            messages.error(request, "Kindly fill the fields")
            return redirect("profile")

        user=request.user
        if request.user.is_authenticated:
            profilemodel = UserBasicInfo()
            profilemodel.full_name = name
            profilemodel.father_name = fathername
            profilemodel.mother_name = mothername
            profilemodel.dob = datetime.strptime(dob,"%Y-%m-%d")
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
            profilemodel.mobile_num = mobile
            profilemodel.parents_num = anumber
            profilemodel.user_id = user.id
            profilemodel.save()

            #profilemodel = UserBasicInfo.objects.filter(full_name=name).first()
            #userimage = UserImage()
            #userimage.name = profilemodel
            #userimage.user_image = photo
            #userimage.user_image_ext = photo.name.split('.')[-1]
            #userimage.save()

            messages.success(request, f'Your data has been added. Now you can take Stream Selection test')
            return redirect('profile')
        else:
            messages.error(request, f'There is some error in your form. Kindly check and fill it again.')
            return redirect('profile')
    else:
        return render(request, 'profile.html')


@login_required
def stream_test(request):
    user = request.user
    try:
        uid = UserBasicInfo.objects.get(user_id=user.id)

        if request.method == 'POST':
            role = request.POST['role_model']
            nature = request.POST['nature']
            com_skills = request.POST['comm_skill']
            development_course = request.POST['dev_course']
            exam_attempts = request.POST['attempt']
            health_issues = request.POST['health']
            drugs = request.POST['drugs']
            school_type = request.POST['school_type']
            attendance = request.POST['attendance']
            scholarship = request.POST['scholarship']

            if role == "" and nature == "" and com_skills == "" and development_course == "" and exam_attempts == "" and health_issues == "" and \
                    drugs == "" and school_type == "" and attendance == "" and scholarship == "":
                messages.error(request, "Kindly fill the fields")
                return redirect("streamtest")
            if request.user.is_authenticated:
                firstmodel = SectionFirst()
                firstmodel.role = role
                firstmodel.nature = nature
                firstmodel.com_skills = com_skills
                firstmodel.development_course = development_course
                firstmodel.exam_attempts = exam_attempts
                firstmodel.health_issues = health_issues
                firstmodel.drugs = drugs
                firstmodel.school_type = school_type
                firstmodel.attendance = attendance
                firstmodel.scholarship = scholarship
                firstmodel.user_id = user.id
                firstmodel.save()

                # check errors

                # success message redirect to result page
                messages.success(request, f'Your data has been recorded. Continue with next section')
                return redirect('section_second')
            else:
                messages.error(request, f'Some error in the form.')
                return redirect('stream_test')
    except UserBasicInfo.DoesNotExist:
        messages.error(request, f'You forgot to fill Student Information form. Kindly fill it first. ')
        return redirect('profile')

    return render(request, 'stream_test.html')


@login_required
def section_second(request):
    user = request.user
    try:
        #uid = SectionFirst.objects.get(user_id=user.id)
        if request.method == 'POST':
            nineth_marks = request.POST['nineth_marks']
            math_nineth_marks = request.POST['math_nineth_marks']
            sci_nineth_marks = request.POST['sci_nineth_marks']
            tenth_marks = request.POST['tenth_marks']
            math_tenth_marks = request.POST['math_tenth_marks']
            sci_tenth_marks = request.POST['sci_tenth_marks']
            math_olympiad = request.POST['math_olympiad']
            sci_olympiad = request.POST['sci_olympiad']
            sci_workshop = request.POST['sci_workshop']
            most_preferred_sub = request.POST['most_preferred_sub']
            least_preferred_sub = request.POST['least_preferred_sub']

            if nineth_marks == "" and math_nineth_marks == "" and sci_nineth_marks == "" and tenth_marks == "" and math_tenth_marks == "" and sci_tenth_marks == "" and \
                    math_olympiad == "" and sci_olympiad == "" and sci_workshop == "" and most_preferred_sub == "" and least_preferred_sub =="" :
                messages.error(request, "Kindly fill the fields")
                return redirect("streamtest")
            if request.user.is_authenticated:
                secondmodel = SectionSecond()
                secondmodel.nineth_marks = nineth_marks
                secondmodel.nineth_marks_math = math_nineth_marks
                secondmodel.nineth_marks_science = sci_nineth_marks
                secondmodel.tenth_marks = tenth_marks
                secondmodel.tenth_marks_math = math_tenth_marks
                secondmodel.tenth_marks_science = sci_tenth_marks
                secondmodel.math_olampaid = math_olympiad
                secondmodel.sci_olampaid = sci_olympiad
                secondmodel.workshop = sci_workshop
                secondmodel.most_perfered_sub = most_preferred_sub
                secondmodel.least_perfered_sub = least_preferred_sub
                secondmodel.user_id = user.id
                secondmodel.save()

                # check errors
                # success message redirect to result page
                messages.success(request, f'Your data has been added.')
                return redirect('result')
            else:
                messages.error(request, f'Some error in the form.')
                return redirect('section_second')
    except SectionFirst.DoesNotExist:
        messages.error(request, f'You forgot to answer the Section First. Answer that first')
        return redirect('stream_test')

    return render(request, 'section_second.html')


def section_three(request):

    render(request, 'section_three.html')


def section_four(request):
    render(request, 'section_four.html')


def section_five(request):
    render(request, 'section_five.html')

def section_six(request):
    render(request, 'section_six.html')


def section_seven(request):
    render(request, 'section_seven.html')

def section_eight(request):
    render(request, 'section_eight.html')


def section_nine(request):
    render(request, 'section_nine.html')

def section_ten(request):
    render(request, 'section_ten.html')


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


@login_required
def checkout(request):
    currency = 'INR'
    amount = 1000  # Rs. 10

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
        user=request.user
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
                amount = 10000  # Rs. 10
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


def error_404_view(request, exception):
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')