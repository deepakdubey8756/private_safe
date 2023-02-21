from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from utilities.authValidation import signup_validation
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
import secrets
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import SinupForm

def genToken():
    """Functions to generate url safe tokens"""
    return secrets.token_urlsafe()

def extract_email_details(request):
    email = request.POST['email']
    password = request.POST["password"]
    confirmPass = request.POST["confirmPass"]
    username = '_'.join(list(email.split('@'))).split('.')[0]
    user = User.objects.filter(username=username)
    status = True
    if len(user)>0:
        status = False
    return {"email": email,
            "password":password,
            "confirmPass": confirmPass,
            "username":username,
            "status":status}


def create_user(details):
    """function to create profile of user"""
    try:
        user = User.objects.create_user(details['username'], details['email'], details['password'])
        user.save()
        token = genToken()
        status = send_mail(details['email'], token, "registration/email_templates.html", "email confirmation", "password_confirm")
        print(status)
        if status:
            profile = Profile(author = user, auth_token=token, isVerfied = False, totalAccess=0)
            profile.save()
        return status
    except Exception as e:
        print("The problem is here", e)
        return False




def signup(request):
    "Check signup validity, create user and send email for verification"
    # # if user is submiting data and it is not authenticated already then do the following...
    if request.method  == 'POST' and not request.user.is_authenticated:
        form = SinupForm(data = request.POST)
        details = extract_email_details(request.POST)

        messages_content = "Please enter the details"
        message_status = messages.INFO
        try:
            if form.is_valid() and details.status and details['confirmPass'] == details['password']:
                status = create_user(details)
                if  status :
                    messages_content = "We have sended you verification email. Please verify."
                    message_status = messages.SUCCESS
                else:
                    raise ValueError("Operation failed")
            else:
                raise ValueError("Either email is not unique or input is not valid")
        except Exception as e:
            messages_content = e
            message_status = messages.ERROR
    

    form = SinupForm()
    messages.add_message(request, message_status, messages_content)
    return render(request, "registration/signup.html", {"form": form})

def confirmPass(request, token):
    """this function confirms verification and login user"""
    if request.user.is_authenticated:
        print("User is authenticated", request.user)
        return redirect('/')
    try:
        # getting profile from token
        profile = Profile.objects.filter(auth_token = str(token))
        if len(profile) == 0:
            messages.add_message(request, messages.ERROR, "Invalid token please do reset password to reconfirm your email")
            return redirect('login')
        
        #verifing user and changing authentication token
        # print("profile: ", profile)
        profile[0].isVerfied = True
        profile[0].auth_token = "none"
        profile[0].totalAccess = 0
        profile[0].save()

        #loging user and sending to home page.
        login(request, profile[0].author)
        messages.add_message(request, messages.SUCCESS, "Email successfully verified")
        return redirect('/')
    
    except Exception as e:
        print(e)
        return HttpResponse("Operation failed!", e)


def send_mail(user_email, token, template_str, subject, domain):
    """Take email and generate token to send it to user"""
    try:
        template = render_to_string(template_str,{
            "token": token,
            "email": user_email,
            "protocol": "http",
            "domain": f"localhost:8000/accounts/{domain}"
        })
        
        email = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            [user_email]
        )
        email.fail_silently = True
        email.send()
        return True
    except Exception as e:
        print(e)
        return False
    

def login_view(request):
    """Function to handle logging user"""
    if request.user.is_authenticated:
        profile = Profile.objects.filter(author = request.user)
        
        if len(profile) == 0 or not profile[0].isVerfied:
            logout(request)
            messages.add_message(request, messages.ERROR, "Error login. Please reset your password")
            return redirect('accounts:reset')
        else:
            return redirect('/')
    elif request.method == "POST" and not request.user.is_authenticated:
        email = request.POST['email']
        password  = request.POST['password']
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect('/')
            
        except Exception as e:
            print(e)
        
        messages.add_message(request, messages.ERROR, "Wrong credentials. Try again")
        return render(request, "registration/login.html")
         
    else :
        print("Rendering page")
        return render(request, "registration/login.html")
    
@login_required
def logout_view(request):
    if request.method=="POST":
        logout(request)
        return redirect('accounts:login')
    return redirect('/')



def reset_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email)
        if len(user) == 0:
            messages.add_message(request, messages.ERROR, "User Not found! please enter correct email")
            return render(request, 'registration/pass_reset.html')

        print("Everything is fine till here......")
        profile = Profile.objects.filter(author = user[0])[0]
        token = genToken()
        profile.auth_token = token
        profile.save()
        print("Printing authentication token, ", profile.auth_token, 'token length', len(token))
        status = send_mail(email, str(token), "registration/reset_pass_email.html", "password reset", "resetconfirm")
        if status:
            messages.add_message(request, messages.SUCCESS, "We have sended you a email please follow along")
        else:
            messages.add_message(request, messages.ERROR, "Operation failed. Retry")
    return render(request, 'registration/pass_reset.html')


def reset_confirm(request, token):
    if request.user.is_authenticated:
        return redirect('/')
    profile = Profile.objects.filter(auth_token=str(token))
    # print(profile)
    if len(profile)==0:
        messages.add_message(request, messages.ERROR, "verificaiton failed. Retry")
        return redirect('accounts:reset')
    if request.method == 'POST':
        password = request.POST['password']
        confirmPass = request.POST['confirmPass']
        message_content = " "
        message_status = ""
        if len(password) < 8:
            message_content = "length should be more than 8"
            message_status = messages.ERROR
        elif password != confirmPass:
            message_content = "passwords are not matching"
            message_status = messages.ERROR
        
        else:
            profile = profile[0]
            profile.isVerfied = True
            profile.auth_token = "none"
            profile.save()
            user = profile.author 
            user.set_password(password)
            user.save()
            messages.add_message(request, messages.SUCCESS, "password reset sucessful. Please consider login")
            return redirect('/accounts/login')
        messages.add_message(request, message_status, message_content)
    return render(request, 'registration/password_reset.html', {'token': str(token)})
