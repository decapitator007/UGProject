from django.shortcuts import render
def home(request):
    return render(request,'delay/home.html',{})
