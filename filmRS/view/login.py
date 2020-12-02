from django.shortcuts import render, redirect

from model.models import User


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    username = request.POST["username"]
    password = request.POST["password"]
    user = User.objects.filter(username=username)
    if user[0].password == password:
        return redirect("/main/")
    return render(request, "login.html")
