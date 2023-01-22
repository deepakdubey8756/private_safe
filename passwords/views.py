from django.shortcuts import render, HttpResponse
import random
import array


MAX_LEN = 12 

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                     'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                     'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                     'z']

UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                     'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                     'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                     'Z']

SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
           '*', '(', ')', '<']

COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + SYMBOLS + LOCASE_CHARACTERS


def genpass():
    #taking one characters from every choices
    rand_digit = random.choice(DIGITS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_symb = random.choice(SYMBOLS)
    temp_pass = rand_digit+rand_lower+rand_symb+rand_upper

    #filling rest of the password with random characters
    for x in range(MAX_LEN-4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)

    #shuffling the final array
    temp_pass_list = array.array('u', temp_pass)
    random.shuffle(temp_pass_list)
    password = ""
    for x in temp_pass_list:
        password = password + x
    return password

def index(request):
    return render(request, 'passwords/index.html')
