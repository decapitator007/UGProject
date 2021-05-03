from django.shortcuts import render,get_object_or_404,redirect
from .forms import inp
from .models import Count
import decimal
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
def uniform(C,g,v,c):
    f=(((1-g)**2)*C)/2
    f/=(1-(g*(v/c)))
    f=round(f,2)
    return f
def overflow(t,c,v):
    f=(((v/c)-1)*t)/2
    f=round(f,2)
    return f
def saturation(a_2w,b_2w,a_3w,b_3w,a_sc,b_sc,a_bc,b_bc,t):
    total=a_2w+b_2w+a_3w+b_3w+a_sc+b_sc+a_bc+b_bc
    x1=((a_2w+b_2w)/total)*100
    x2=((a_3w+b_3w)/total)*100
    x3=((a_sc+b_sc)/total)*100
    x4=((a_bc+b_bc)/total)*100
    x5=((a_2w+a_3w+a_sc+a_bc)/total)*100
    x6=total/t
    f=decimal.Decimal(0.031)*decimal.Decimal(x1)-decimal.Decimal(0.019)*decimal.Decimal(x2)+decimal.Decimal(0.009)*decimal.Decimal(x3)
    f+=decimal.Decimal(0.034)*decimal.Decimal(x4)+decimal.Decimal(0.013)*decimal.Decimal(x5)+decimal.Decimal(3.752)*decimal.Decimal(x6)
    f=round(f,2)
    return f
def phase(v1,v2,s1,s2,t,C,g):
    c1=s1*g
    c2=s2*g
    r1=v1/c1
    r2=v2/c2
    if r1<=1:
        d1=uniform(C,g,v1,c1)
    else:
        d1=uniform(C,g,v1,v1)+overflow(t,c1,v1)
    if r2<=1:
        d2=uniform(C,g,v2,c2)
    else:
        d2=uniform(C,g,v2,v2)+overflow(t,c2,v2)
    f=(d1*v1+d2*v2)/(v1+v2)
    f=round(f,2)
    return f
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
            s1=saturation(entry.a_2w,entry.b_2w,entry.a_3w,entry.b_3w,entry.a_sc,entry.b_sc,entry.a_bc,entry.b_bc,t)
            s2=saturation(entry.c_2w,entry.d_2w,entry.c_3w,entry.d_3w,entry.c_sc,entry.d_sc,entry.c_bc,entry.d_bc,t)
            s3=saturation(entry.e_2w,entry.f_2w,entry.e_3w,entry.f_3w,entry.e_sc,entry.f_sc,entry.e_bc,entry.f_bc,t)
            s4=saturation(entry.g_2w,entry.h_2w,entry.g_3w,entry.h_3w,entry.g_sc,entry.h_sc,entry.g_bc,entry.h_bc,t)
            p1=phase((entry.b_2w+entry.b_3w+entry.b_sc+entry.b_bc)/t,(entry.f_2w+entry.f_3w+entry.f_sc+entry.f_bc)/t,s1,s3,t,C,g)
            p2=phase((entry.a_2w+entry.a_3w+entry.a_sc+entry.a_bc)/t,(entry.e_2w+entry.e_3w+entry.e_sc+entry.e_bc)/t,s1,s3,t,C,g)
            p3=phase((entry.d_2w+entry.d_3w+entry.d_sc+entry.d_bc)/t,(entry.h_2w+entry.h_3w+entry.h_sc+entry.h_bc)/t,s2,s4,t,C,g)
            p4=phase((entry.c_2w+entry.c_3w+entry.c_sc+entry.c_bc)/t,(entry.g_2w+entry.g_3w+entry.g_sc+entry.g_bc)/t,s2,s4,t,C,g)
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
