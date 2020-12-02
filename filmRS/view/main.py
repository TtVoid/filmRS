from django.shortcuts import render

from model.models import Movies

def main(request):
    context={}
    context['films']=Movies.objects.all().order_by("-release_time")[:20]
    print(context['films'][0].intro)
    return render(request, "main.html",context)
