# Main docs

Note: This docs contains information related to Core  functionalities of private safe

Core working contains..
1. Retrieving  password notes and displaying it.
2. Adding new password notes
3. Copying password
4. Delete passwords
5. Showing number to times user has accessed their notes.
6. Regenrate passwords
Note: For any kind of operation related to main functionalities requres user to logged in.

>To read it's source code consider going to passwords/views.py

### Retriving password notes 
This is handled by function `index` which first check if logged user is verified. It then scrape data from `notes` model and `count access` model(to know more about them check model's docs)

### Adding password notes

This handles functionalities related new password notes.
It takes input as `name`, `email` and `password` ( a pregenerated random password)
Validate it and save it into databse . and finaly return to home page.

### Regenrate password
Here we are using python's `secrets module` to generate random uniqe passwords
containing `letter`, `symbols` and `numbers`. 
