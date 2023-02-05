import string, secrets

def genpass():
    """function to generate random passwords"""
    MAX_LEN = 12
    password = ""
    Symbols = "@#$%*&^{}()_<?>"
    combined_alphabet = string.ascii_letters + string.digits + Symbols
    while True:
        password = ''.join(secrets.choice(combined_alphabet) for i in range(MAX_LEN))
        if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3):
            break
    return password
