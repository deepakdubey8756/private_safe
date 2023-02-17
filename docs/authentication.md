#Authentication docs

Note: This docs contains information related to authentication functionalities.

Authentication contains ...	
1. Registering user and email confirmation.
2. Login and logout functionalities.
3.  Password reset functionalitiy.

>To read it's source code consider going to accounts/views.py

## Registering user and email confirmation
Following is the working of creating user.
###1. Taking data and checking it's validation.

 Taking data from `request` is done by `extract_email_details` function. 
 
###2.  Checking if email is unique and data is valid or not.
  validation of email and  passwords are done by `signup_validation` function which takes details as   a dictionary containing `email`, `passwords` and other details.
### If step 2 fails then returning signup page with error message.
###3. If step 2 is fine then create profile and send email to verify user.
profile creation is done by function `create_user` which takes neccesary details such as emails and passwords as input and create user. 
To confirm email verification we are generating a unique `auth-token` and sending it to user through `smtp server`. 
`Authentication token ` is stored in `profile model` (to know more about it consider reading models docs).

###4. Email varification 
Email verification is done by `confirmPass` which takes `auth-token` from `url` as a parameter and match it with tokens stored in any of profile model. if there is a match then set profile as verified else return `HTTP` response as operation failed.

###5. Login user and redirect to home page

After everything is fine then `login user` and `redirect` them to home page.


## Login and logout

### Login
Functionalities related to loging user is handled by login_view function which checks following things.
1. Any profile with this email exists or not. 
2. Profile is verified or not.
3. Enter password is correct or not. 
If everything is correct then it log user and redirect him to the home page.
else it redirect to login page with error message.


###Logout 
Logout is handled with function logout view which lougout user and redirect request to login page.

##3. Password reset

Reseting password is done by two funcitons
1. `reset_view` :   which first check  if is there any profile with this email and then send verification email to user's email to check whether it ts the user who is  trying to reset the password.

2. `reset_confirm` :  which take sended `auth-token` and return a page to enter new passwords and then it reset password with verified autheticated token.

