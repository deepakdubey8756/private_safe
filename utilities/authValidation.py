def signup_validation(values):
    result = {"status": True, "message": ""}

    if values['email'] == None or values['password'] == None:
        result['status'] = False
        result['message']  = "fill the forms correctly"
    
    elif values['password'] != values['confirmPass']:
        result['status']  = False
        result['message']  = "Passwords are not matching"
    
    elif len(values['password']) <= 8:
        result['status'] = False
        result['message'] = "Password length should be more than 8"
    
    elif values['user']:
        result['status'] = False
        result['message']  = "User already exists"
    return result