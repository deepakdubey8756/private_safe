#Models docs

Note: This docs contains information related to Models

Private Safe contains three models. 
### 1. Profile
This model contains two field 
1. `Autho`:  Information about user form django's user model
2. `Auth-token`: Used to store token sended as email to user.
3. `is_verified`: To check if user is authenticated to not.

This models is used in verify email authenticity.

### 2. Notes
This models contains following field
1. `Author` = Information about user form django's user model
2. `name` = Name of the account password is begin saved.
3. `username` = Useranme of the account.
4. `Password` = password manager.
5. `date_modified`: Last date on which password is modified.

This is our primary databse where account information is stored.



### CountAccess
This model stores total number of times an account  is being accessed.
