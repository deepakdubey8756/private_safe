#Intro

Private safe is a secure and stateless password manager. 
A place where you can manage your passwords secretly.

This docs contains following segments..

0. Tech stack used.
1. Design and features.                
2. Detailed explaination of working functionality with source code.
3. Contribution guildlines.

## Tech stack used

1. `Django`: As a backend system. 
2. `Django-templates`: to render pages.
3. `Html, css, javaScript, bootstrap`:--- for frontent ui work.
4. `sqlite`: Using default django.
5. `Django messaging framework`: This includes functionalities related to internal messaging.
##Design and Architecture of working functionalities

The architecture of the project is divided into following components.

1. Authentication:
    Handles functionalities related to authentication and authorization. like:--
    1. Create user. 
    2. Login user.
    3. Email verification.
    4. Password reset .
	5. login,  logout etc.
>To know more about it consider reading authetication docs.

2.   Core Functions:
This is where our main working functionalities of projects lies.
It includes :
	1. Creating passwords notes.
	2. Generting random passwords.
	3. Copying passwords and deleting them.
> to know more about it consider reading core docs.

3.  Models
	It includes different models and database realation neccesary for our functionalities.
	>to know more about it consider reading models docs.


4. Testing.
Includes testing of every working functionality.


5. Docs..
Docs containing technical details and logic.








