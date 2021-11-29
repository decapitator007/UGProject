from django.shortcuts import render
from .forms import inp
import decimal,math,openpyxl
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io,urllib,base64,numpy as np
def uniform(C,g,v,c):
    X=(v/c)
    if X>1:
        X=1
    f=(((1-g)**2)*C)/2
    f/=(1-(g*X))
    f=round(f,2)
    return f
def overflow(t,c,v):
    f=(((v/c)-1)*t)/2
    f=round(f,2)
    return f
def ak_overflow(t,c,v,s,g):
    X=((s*g)/600)+decimal.Decimal(0.67)
    x=v/c
    od=(12*(x-X))/(c*t)
    od=od+(x-1)*(x-1)
    od=math.sqrt(abs(od))
    od=decimal.Decimal(od)+(x-1)
    od=od*(c*t)
    od=od/4
    return od
def pcu(a,b,c,d):
    f=decimal.Decimal(0.5)*decimal.Decimal(a)+decimal.Decimal(0.8)*decimal.Decimal(b)+decimal.Decimal(c)+decimal.Decimal(d)*decimal.Decimal(3.5)
    f=round(f,2)
    return f
def saturation(a_2w,b_2w,a_3w,b_3w,a_sc,b_sc,a_bc,b_bc,t):
    total=a_2w+b_2w+a_3w+b_3w+a_sc+b_sc+a_bc+b_bc
    x1=((a_2w+b_2w)/total)*100
    x2=((a_3w+b_3w)/total)*100
    x3=((a_sc+b_sc)/total)*100
    x4=((a_bc+b_bc)/total)*100
    x5=((a_2w+a_3w+a_sc+a_bc)/total)*100
    x6=pcu(a_2w+b_2w,a_3w+b_3w,a_sc+b_sc,a_bc+b_bc)/t
    f=decimal.Decimal(0.031)*decimal.Decimal(x1)-decimal.Decimal(0.019)*decimal.Decimal(x2)+decimal.Decimal(0.009)*decimal.Decimal(x3)
    f+=decimal.Decimal(0.034)*decimal.Decimal(x4)+decimal.Decimal(0.013)*decimal.Decimal(x5)+decimal.Decimal(3.752)*decimal.Decimal(x6)
    f=round(f,2)
    return f
def ak_phase(v1,v2,s1,s2,t,C,g):
    c1=s1*g
    c2=s2*g
    r1=v1/c1
    r2=v2/c2
    if r1<=1:
        d1=uniform(C,g,v1,c1)
    else:
        d1=uniform(C,g,v1,v1)+ak_overflow(t,c1,v1,s1,g*C)
    if r2<=1:
        d2=uniform(C,g,v2,c2)
    else:
        d2=uniform(C,g,v2,v2)+ak_overflow(t,c2,v2,s2,g*C)
    f=(d1*v1+d2*v2)/(v1+v2)
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
    if request.method=="POST":
        form=inp(request.POST)
        if form.is_valid():
            g1=form.cleaned_data.get("g_1")
            g2=form.cleaned_data.get("g_2")
            g3=form.cleaned_data.get("g_3")
            g4=form.cleaned_data.get("g_4")
            C=g1+g2+g3+g4+20
            g1/=C
            g2/=C
            g3/=C
            g4/=C
            ans1=list()
            ans2=list()
            ans3=list()
            ans4=list()
            time=list()
            excel_file=request.FILES["excel_file"]
            wb=openpyxl.load_workbook(excel_file)
            worksheet=wb["Sheet1"]
            for row in worksheet.iter_rows():
                row_data=list()
                for cell in row:
                    row_data.append(int(str(cell.value)))
                t=row_data[0]
                s1=saturation(row_data[1],row_data[5],row_data[2],row_data[6],row_data[3],row_data[7],row_data[4],row_data[8],t)
                s2=saturation(row_data[9],row_data[13],row_data[10],row_data[14],row_data[11],row_data[15],row_data[12],row_data[16],t)
                s3=saturation(row_data[17],row_data[21],row_data[18],row_data[22],row_data[19],row_data[23],row_data[20],row_data[24],t)
                s4=saturation(row_data[25],row_data[29],row_data[26],row_data[30],row_data[27],row_data[31],row_data[28],row_data[32],t)
                p1=phase(pcu(row_data[5],row_data[6],row_data[7],row_data[8])/t,pcu(row_data[21],row_data[22],row_data[23],row_data[24])/t,s1,s3,t,C,g1)
                p2=phase(pcu(row_data[1],row_data[2],row_data[3],row_data[4])/t,pcu(row_data[17],row_data[18],row_data[19],row_data[20])/t,s1,s3,t,C,g2)
                p3=phase(pcu(row_data[13],row_data[14],row_data[15],row_data[16])/t,pcu(row_data[29],row_data[30],row_data[31],row_data[32])/t,s2,s4,t,C,g3)
                p4=phase(pcu(row_data[9],row_data[10],row_data[11],row_data[12])/t,pcu(row_data[25],row_data[26],row_data[27],row_data[28])/t,s2,s4,t,C,g4)
                p5=ak_phase(pcu(row_data[5],row_data[6],row_data[7],row_data[8])/t,pcu(row_data[21],row_data[22],row_data[23],row_data[24])/t,s1,s3,t,C,g1)
                p6=ak_phase(pcu(row_data[1],row_data[2],row_data[3],row_data[4])/t,pcu(row_data[17],row_data[18],row_data[19],row_data[20])/t,s1,s3,t,C,g2)
                p7=ak_phase(pcu(row_data[13],row_data[14],row_data[15],row_data[16])/t,pcu(row_data[29],row_data[30],row_data[31],row_data[32])/t,s2,s4,t,C,g3)
                p8=ak_phase(pcu(row_data[9],row_data[10],row_data[11],row_data[12])/t,pcu(row_data[25],row_data[26],row_data[27],row_data[28])/t,s2,s4,t,C,g4)
                ans1.append(p1)
                ans2.append(p2)
                ans3.append(p3)
                ans4.append(p4)
                time.append(t)
            plt.plot(time,ans1,marker='o',linestyle='--',color='r')
            # plt.xticks(np.arange(min(time),max(time)+1,0.5))
            # plt.yticks(np.arange(math.floor(min(ans1)),math.ceil(max(ans1))+1,1))
            plt.title("Phase 1")
            plt.ylabel("Average Delay (sec/veh)")
            plt.xlabel("Time (sec)")
            fig=plt.gcf()
            buf=io.BytesIO()
            fig.savefig(buf,format='png')
            buf.seek(0)
            string=base64.b64encode(buf.read())
            uri1=urllib.parse.quote(string)
            plt.clf()
            plt.plot(time,ans2,marker='o',linestyle='--',color='r')
            plt.title("Phase 2")
            plt.ylabel("Average Delay (sec/veh)")
            plt.xlabel("Time (sec)")
            fig=plt.gcf()
            buf=io.BytesIO()
            fig.savefig(buf,format='png')
            buf.seek(0)
            string=base64.b64encode(buf.read())
            uri2=urllib.parse.quote(string)
            plt.clf()
            plt.plot(time,ans3,marker='o',linestyle='--',color='r')
            plt.title("Phase 3")
            plt.ylabel("Average Delay (sec/veh)")
            plt.xlabel("Time (sec)")
            fig=plt.gcf()
            buf=io.BytesIO()
            fig.savefig(buf,format='png')
            buf.seek(0)
            string=base64.b64encode(buf.read())
            uri3=urllib.parse.quote(string)
            plt.clf()
            plt.plot(time,ans4,marker='o',linestyle='--',color='r')
            plt.title("Phase 4")
            plt.ylabel("Average Delay (sec/veh)")
            plt.xlabel("Time (sec)")
            fig=plt.gcf()
            buf=io.BytesIO()
            fig.savefig(buf,format='png')
            buf.seek(0)
            string=base64.b64encode(buf.read())
            uri4=urllib.parse.quote(string)
            plt.clf()
            mylist=zip(time,ans1,ans2,ans3,ans4)
            return render(request,'delay/index.html',{"data1":uri1,"data2":uri2,"data3":uri3,"data4":uri4,"mylist":mylist})
    else:
        form=inp()
        return render(request,'delay/home.html',{'form':form})
