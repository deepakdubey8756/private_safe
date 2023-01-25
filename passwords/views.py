from django.shortcuts import render, HttpResponse, redirect
from .models import Note
import random
import array
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

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


@login_required
def index(request):
    if request.user.is_authenticated:
        print(request.user)
        note = Note.objects.filter(request.user)
        total = len(note)
        #calculating number of time this site is visited
        num_visits = request.session.get('num_visits', 0)
        request.session['num_visits'] = num_visits + 1
        context = {"notes": note, "total": total, "visits":num_visits}
        return render(request, 'passwords/index.html', context)
    return redirect('login')

@login_required
def delete(request, id):
    if request.method == "POST":
        try:
            note = Note.objects.get(id=id)
            note.delete()
            return redirect('/')
        except Exception as e:
            print(e)
    return HttpResponse("Failed! Some Error Occured")

@login_required
def regen(request, id):
    if request.method == "POST":
        try:
            note = Note.objects.get(id=id)
            note.password = genpass()
            note.save()
            return redirect('/')
        except Exception as e:
            print(e)
    return HttpResponse("Failed! Some error occured")

@login_required
def addPass(request):
    if request.method == "POST":
        name = request.POST["name"]
        username = request.POST["username"]
        password = request.POST["password"]
        print({"name":name, "username": username, "password": password})
        if name=="xyz" or username=="xyz":
            return HttpResponse("Please fill the names and usernames correctly")
        note = Note(author=request.user, name=name, username=username, password=password)
        note.save()
        return redirect('/')
    context  = {"pass": genpass()}
    return render(request, "passwords/newEntry.html", context)




