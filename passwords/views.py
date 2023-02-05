from django.shortcuts import render, HttpResponse, redirect
from .models import Note, CountAcess
from accounts.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utilities.genpass import genpass

def isprofile_verified(user):
    profile = Profile.objects.filter(author=user)
    if len(profile) > 0:
        return profile[0].isVerfied
    return False



@login_required
def index(request):
    if request.user.is_authenticated:
            profile = Profile.objects.filter(author=request.user)
            if not profile[0].isVerfied:
                messages.add_message(request, messages.ERROR, "Please verify your email")
                return redirect('accounts:login')
            note = Note.objects.filter(author = request.user)
            visits = 0
            try:
                counts = CountAcess.objects.get(author=request.user)
                counts.total += 1
                counts.save()
                visits = counts.total
            except CountAcess.DoesNotExist:
                counts = CountAcess(author=request.user)
                counts.save()
                visits = 1
            total = len(note)
            context = {"notes": note, "total": total, "visits": visits, "user": request.user}
            return render(request, 'passwords/index.html', context)
    return redirect('accounts:login')

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
    profile = Profile.objects.filter(author = request.user)
    if len(profile) == 0:
       messages.add_message("your email is not verified yet. Please login first")
       return redirect("password:login")

    if request.method == "POST":
        name = request.POST["name"]
        username = request.POST["username"]
        password = request.POST["password"]
        print({"name":name, "username": username, "password": password})
        if name=="xyz" or username=="xyz":
            messages.add_message(request, messages.error, "please fill the form correctly")
            return render(request, )
        note = Note(author=request.user, name=name, username=username, password=password)
        note.save()
        return redirect('/')
    context  = {"pass": genpass()}
    return render(request, "passwords/newEntry.html", context)



