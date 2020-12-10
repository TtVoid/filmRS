from django.shortcuts import render, redirect

from model.models import Movies


def logout(request):
    request.session.flush()
    return redirect("/login/")


def search(request):
    movieName = request.POST["movieName"]
    # print(movieName)

    context = {}
    context['status']='search'
    context['films'] = Movies.objects.filter(name__icontains=movieName)  # 根据 id查询 movie

    return render(request, "films.html", context)
