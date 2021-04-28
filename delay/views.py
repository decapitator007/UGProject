from django.shortcuts import render,get_object_or_404,redirect
from .forms import inp
from .models import Count
def zero(entry):
    entry.a_2w=0
    entry.a_3w=0
    entry.a_sc=0
    entry.a_bc=0
    entry.b_2w=0
    entry.b_3w=0
    entry.b_sc=0
    entry.b_bc=0
    entry.c_2w=0
    entry.c_3w=0
    entry.c_sc=0
    entry.c_bc=0
    entry.d_2w=0
    entry.d_3w=0
    entry.d_sc=0
    entry.d_bc=0
    entry.e_2w=0
    entry.e_3w=0
    entry.e_sc=0
    entry.e_bc=0
    entry.f_2w=0
    entry.f_3w=0
    entry.f_sc=0
    entry.f_bc=0
    entry.g_2w=0
    entry.g_3w=0
    entry.g_sc=0
    entry.g_bc=0
    entry.h_2w=0
    entry.h_3w=0
    entry.h_sc=0
    entry.h_bc=0
    entry.save()
def home(request):
    p1=0
    p2=0
    p3=0
    p4=0
    entry=get_object_or_404(Count,pk=1)
    if request.method=="POST" and 'calculate' in request.POST:
        form=inp(request.POST)
        if form.is_valid():
            g=form.cleaned_data.get("g_c")
            t=form.cleaned_data.get("t")
            C=form.cleaned_data.get("C")
            p1=p2=p3=p4=g+t+C
    elif request.method=="POST":
        form=inp()
        if 'a_2w' in request.POST:
            entry.a_2w+=1
        if 'a_3w' in request.POST:
            entry.a_3w+=1
        if 'a_sc' in request.POST:
            entry.a_sc+=1
        if 'a_bc' in request.POST:
            entry.a_bc+=1
        if 'b_2w' in request.POST:
            entry.b_2w+=1
        if 'b_3w' in request.POST:
            entry.b_3w+=1
        if 'b_sc' in request.POST:
            entry.b_sc+=1
        if 'b_bc' in request.POST:
            entry.b_bc+=1
        if 'c_2w' in request.POST:
            entry.c_2w+=1
        if 'c_3w' in request.POST:
            entry.c_3w+=1
        if 'c_sc' in request.POST:
            entry.c_sc+=1
        if 'c_bc' in request.POST:
            entry.c_bc+=1
        if 'd_2w' in request.POST:
            entry.d_2w+=1
        if 'd_3w' in request.POST:
            entry.d_3w+=1
        if 'd_sc' in request.POST:
            entry.d_sc+=1
        if 'd_bc' in request.POST:
            entry.d_bc+=1
        if 'e_2w' in request.POST:
            entry.e_2w+=1
        if 'e_3w' in request.POST:
            entry.e_3w+=1
        if 'e_sc' in request.POST:
            entry.e_sc+=1
        if 'e_bc' in request.POST:
            entry.e_bc+=1
        if 'f_2w' in request.POST:
            entry.f_2w+=1
        if 'f_3w' in request.POST:
            entry.f_3w+=1
        if 'f_sc' in request.POST:
            entry.f_sc+=1
        if 'f_bc' in request.POST:
            entry.f_bc+=1
        if 'g_2w' in request.POST:
            entry.g_2w+=1
        if 'g_3w' in request.POST:
            entry.g_3w+=1
        if 'g_sc' in request.POST:
            entry.g_sc+=1
        if 'g_bc' in request.POST:
            entry.g_bc+=1
        if 'h_2w' in request.POST:
            entry.h_2w+=1
        if 'h_3w' in request.POST:
            entry.h_3w+=1
        if 'h_sc' in request.POST:
            entry.h_sc+=1
        if 'h_bc' in request.POST:
            entry.h_bc+=1
        if 'reset' in request.POST:
            zero(entry)
        entry.save()
    else:
        form=inp()
        zero(entry)
    return render(request,'delay/home.html',{'entry':entry,'form':form,'p1':p1,'p2':p2,'p3':p3,'p4':p4})
