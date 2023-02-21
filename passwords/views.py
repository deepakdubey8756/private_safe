from django.shortcuts import render, HttpResponse, redirect
from .models import Note
from accounts.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utilities.genpass import genpass
from .forms import NoteForm




@login_required
def index(request):
    profile = Profile.objects.get(author=request.user)
    if not profile.isVerfied:
        messages.add_message(request, messages.ERROR, "Please verify your email")
        return redirect('accounts:reset')
    note = Note.objects.filter(author = request.user)
    profile.totalAccess = profile.totalAccess + 1
    profile.save()
    context = {"notes": note, "total": len(note), "visits": profile.totalAccess, "user": request.user}
    return render(request, 'passwords/index.html', context)


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

    if len(profile) == 0 or not profile[0].isVerfied:
       messages.add_message("Please verify your email first")
       return redirect("accounts:reset")
    
    if request.method == "POST":
        form = NoteForm(data = request.POST)
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        print("name:", name, "username: ", username, "password: ", password)
        if form.is_valid():
            note = Note(author=request.user, name=name, username=username, password=password)
            note.save()
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, "please fill the form correctly")
    form = NoteForm()
    context  = {"pass": genpass(), "form": form}
    return render(request, "passwords/newEntry.html", context)



