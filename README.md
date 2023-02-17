# Private Safe

  

A simple website written in `django` to store `username` and `passwords`.

It comes with full custom authentication and authorization to secure user credentials from being stolen.

  

## Installation

  

Clone the source code into desired directory and then run following commands.

  

```bash

#0. Get into directry.
cd privateSafe
#1. Initialize virutal envirment.
#this project uses python3
python3 -m venv myvenv
#2. Activate it.
source myvenv/bin/activate
#3. Install django in it.
pip3 install django
#4. create a directory to store credentials...
touch credentials.py
#5. store email credentials to send emails to user.
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'youremail'
EMAIL_HOST_PASSWORD = 'app-passwords'
SECRET_KEY = 'django-insecure-n%2#4_i$cs%4xj=@b!t#6pgjj8q&hfmp3a^d*xt6d%61f+cwy2'
#Now run the project
python3 manage.py runserver
```
  

## Application Details

Private safe is manly used to store and maintain username and passwords.
It comes with full user authentication for security.

>>For more technical and design details consider reading docs.


## Contributing


Pull requests are welcome. For major changes, please open an issue first

to discuss what you would like to change.

Please make sure to update tests as appropriate.
  
## Future scope:
Currently we are using only email confirmation to check authenticity of accounts. 
But in future we will add more funcitonalities to make it more secure.


## License

 
[MIT](https://choosealicense.com/licenses/mit/)
