from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseNotFound
from .form import UserAdminform,Setpassword
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from .utils import generate_token,generate_pass_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str,  DjangoUnicodeDecodeError
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.mail import EmailMessage
import email
import threading
from django.urls import reverse
from django.conf import settings
from .models import CustomUser,Profile
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_activation_email(user,password,request):
    current_site = get_current_site(request)
    email_subject = 'Registration Info'
    email_body = render_to_string('account/activate_email.html', {
        'user': user.username,
        'firstname':user.first_name,
        'password':password,
        'domain': current_site,
        
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email='support@assetssecurityledgers.com',
                         to=[user.email]
                         )
    if not settings.TESTING:
        EmailThread(email).start()




def send_change_password_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Reset your password'
    email_body = render_to_string('account/change_forget_pass.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_pass_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email='support@assetssecurityledgers.com',
                         to=[user.email]
                         )
    if not settings.TESTING:
        EmailThread(email).start()




def send_alert_email_user_registration(user):
    
    email_subject = 'New account created'
    email_body = render_to_string('account/alert_user_reg.html', {
        'user': user,
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email='support@assetssecurityledgers.com',
                         to=["johnsimonwork@gmail.com"]
                         )
    if not settings.TESTING:
        EmailThread(email).start()


def support_message_email(user,message):
    
    email_subject = 'Support Message'
    email_body = render_to_string('account/support_message.html', {
        'user': user,
        'message': message,
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email='support@assetssecurityledgers.com',
                         to=[user.email]
                         )
    if not settings.TESTING:
        EmailThread(email).start()


def register_user(request):
    profile_id = request.session.get('ref_profile_id')
    user_form=UserAdminform()

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        user_form = UserAdminform(request.POST)
        # check whether it's valid:
        if user_form.is_valid():
            if profile_id is not None:
                recommended_profile = Profile.objects.get(id=profile_id)
                password = user_form.cleaned_data['password1']
                
                user_reg = user_form.save()
                registered_user = CustomUser.objects.get(id=user_reg.id)
                registered_user_profile = Profile.objects.get(user=registered_user)
                registered_user_profile.recommended_by = recommended_profile.user
                registered_user_profile.save()
                send_activation_email(user_reg,password,request)
                messages.success(request,"Created! now login to continue")
                return redirect('account:login_user')
            else:
                password = user_form.cleaned_data['password1']
                
                user_reg = user_form.save()
                
                
                send_activation_email(user_reg,password,request)
                messages.success(request,"Created! now login to continue")
                return redirect('account:login_user')

            
    return render(request,"account/register.html",{"user_form":user_form})


def activate_user_email(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = CustomUser.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        send_alert_email_user_registration(user)

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('account:login_user'))

    return render(request, 'account/activate-failed.html', {"user": user})


def login_user(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password1")
        user= authenticate(request, username=username,password=password)
        if user is not None:
             
            login(request,user,)
            messages.success(request,("login successfully"))
            return redirect('dashboard:dashboard-page')
            
        messages.error(request,("incorrect username/password try again"))
        return redirect('account:login_user')

        
            
    return render(request,"account/login.html")


def forget_password(request):
    if request.method == 'POST':
        email=request.POST.get('email')

        try:
            user = CustomUser.objects.get(email=email)
            send_change_password_email(user,request)
            messages.success(request,("Password reset link have been sent to your email"))  
            return redirect(reverse('account:login_user')) 
        except:
            messages.error(request,("email does not exists"))
        
    return render(request, 'account/forget_password_form.html')


def reset_password(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        
        user = CustomUser.objects.get(pk=uid)

    except Exception as e:
        user = None
    
    if user and generate_pass_token.check_token(user, token):
        request.session['id'] = int(uid)
        return redirect(reverse('account:to_reset_pass')) 
    return render(request, 'account/reset_failed.html', {"user": user})


def to_reset_password(request):
    user_id=request.session.get('id')
    if user_id is not None:
        print(user_id)
        change_pass_form =Setpassword()
        if request.method == 'POST':
            user = CustomUser.objects.get(pk=user_id)
            change_pass_form =Setpassword(request.POST)  
            if change_pass_form.is_valid():
                password1 = change_pass_form.cleaned_data.get('new_password1')
                user.set_password(password1)
                user.save()
                messages.success(request,("Reset password was successful"))
                return redirect(reverse('account:login_user')) 
        return render(request,'account/change_pass.html',{"change_pass_form":change_pass_form})
    else:
        return HttpResponseNotFound()


def referral(request,*args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profiles = Profile.objects.get(profile_name=code)
        request.session['ref_profile_id'] = profiles.id
    except:
        pass
    return redirect(reverse('account:register_user')) 


def logout_view(request):
    logout(request)
    return redirect('account:home_page')
    
@login_required
def account_setting(request):
    user = request.user
    password_change_form = PasswordChangeForm(user)
    if request.method =="POST":
        setting_name = request.POST.get("setting_name")
        if setting_name == "personal":
            user_account = CustomUser.objects.get(id=user.id)
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            phone_number = request.POST.get("phone_number")
            user_account.first_name = first_name
            user_account.last_name = last_name
            user_account.phone_number = phone_number
            user_account.save()
            messages.success(request,'your profile have been updated successfully')
            return redirect('account:account_setting')
        elif setting_name == "password": 
            password_change_form = PasswordChangeForm(user, request.POST)
            if password_change_form.is_valid():
                password_change_form.save()
                messages.success(request, "Your password has been changed")
                return redirect('account:account_setting')
            else:
                messages.error(request, "failed! change of password try again")
                redirect('account:account_setting')

    return render(request,"account/account_setting.html",{"password_change_form":password_change_form,"user":user})


@login_required
def support(request):
    if request.method=="POST":
        message = request.POST.get("message")
        user=request.user
        support_message_email(user,message)
        messages.success(request,'message sent')
    return render(request, 'account/support.html')


def home_page(request):
    return render(request, 'account/index.html')


def about_page(request):
    return render(request, 'account/about.html')


def contact_page(request):
    return render(request, 'account/contact.html')


def faq_page(request):
    return render(request, 'account/FAQ.html')


def tc_page(request):
    return render(request, 'account/terms_&_conditions.html')
