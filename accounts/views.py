from django.shortcuts import render, HttpResponse, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from utilities.authValidation import signup_validation
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
import secrets
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def genToken():
    """Functions to generate url safe tokens"""
    return secrets.token_urlsafe()

def extract_email_details(request):
    email = request.POST['email']
    password = request.POST["password"]
    confirmPass = request.POST["confirmPass"]
    username = list(email.split('@'))[0]
    user = User.objects.filter(username=username)
    if len(user)>0:
        username = username+'1'
    return {"email": email, "password":password, "confirmPass": confirmPass, "username":username}


def create_user(details):
    """function to create profile of user"""
    try:
        user = User.objects.create_user(details['username'], details['email'], details['password'])
        user.save()
        token = genToken()
        status = send_mail(details['email'], token, "registration/email_templates.html", "email confirmation", "password_confirm")
        print(status)
        if status:
            profile = Profile(author = user, auth_token=token, isVerfied = False)
            profile.save()
        return status
    except Exception as e:
        print("The problem is here", e)
        return False




def signup(request):
    """view to handle signing user
    Functionality:
        1. Get data from request and save it in a dictionary.
        2. Check if email is unique and data is valid
        3. If step 2 failed then return to the page with error message.
        4. If everything is fine then save user and send email with token to confirm its identity."""
    print("Here is everything that matters")
    # if user is submiting data and it is not authenticated already then do the following...
    if request.method  == 'POST' and not request.user.is_authenticated:

        #1. Get the data from request and save it in a dictionary
        details = extract_email_details(request)
        details['user'] = False
        print("deatils", details)

        #2. check if email is unique and data is valid.
        try:
            user = User.objects.filter(email=details['email'])
            if len(user) > 0:
                details['user'] = True
        except Exception as e:
            print(e)

        #validate credenctials and check if user is already exits or not.
        checkPass = signup_validation(details)


        #3. If everything is fine then create the user else return with error message

        message_content = ""
        message_status = ""
        if checkPass['status'] == False:
            message_content = checkPass['message']
            message_status = messages.ERROR
        else:
            user = create_user(details)
            if user:
                message_content = "We have sended you a verification email. Please verify your email"
                message_status = messages.SUCCESS
            else:
                message_content = "Operation failed try again"
                message_status = messages.ERROR

        messages.add_message(request, message_status, message_content)
        return render(request, 'registration/signup.html')


    #4. handling case when user is already authenticated or request is not post
  
    if request.user.is_authenticated:
        return redirect('/')
    
    messages.add_message(request, messages.INFO, 'please enter your email and passwords')
    return render(request, "registration/signup.html")


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
        print("profile: ", profile)
        profile[0].isVerfied = True
        profile[0].auth_token = "none"
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
    print(profile)
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
