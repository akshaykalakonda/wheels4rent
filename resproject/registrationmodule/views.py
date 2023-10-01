import re
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Registration, Admin, CarBooking
from .forms import CarsForm,ContactForm
from .models import Registration, CarModels, Contact
from django.views.decorators.cache import cache_control
from datetime import datetime
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth import logout
from django.shortcuts import render, redirect


# Create your views here.
def save_register(request):
    if request.method=='POST':
        name = request.POST['name']
        emailid = request.POST['emailid']
        contactno = request.POST['contactno']
        password=request.POST['password']
        con_password=request.POST['password-repeat']
        try:
            if password == con_password:
                if (len(password) >= 8):
                    if (bool(re.match('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,30})', password)) == True):
                        msg = "Registration Successful !! Login Here !!"
                        userobj = Registration(fullname=name,email=emailid,contact=contactno,password=password)
                        Registration.save(userobj)
                        return render(request, "login.html",{"msg": msg})
                    else:
                        msg="Password must contain atleast one number [0-9],uppercase [A-Z],special character [!@#$%^&*]!! try again!!"
                        return render(request,"registration.html",{"msg":msg})
                else:
                    msg="     Password Length should be >=8 !! try again!!"
                    return render(request,"registration.html",{"msg":msg})
            else:
                msg = '               Password and Confirm Password Does Not Match !! try again!!'
                return render(request, "registration.html", {"msg": msg})

        except Exception as e:
            return render(request,"registration.html",{"msg":"Email Already Exists"})

def test(request):
    return render(request,"login.html")

def checkuserlogin(request):
    if request.method == "POST":
            emailid=request.POST["emailid"]
            pwd=request.POST["password"]
            if Admin.objects.filter(Q(email=emailid) & Q(password=pwd)):
                return render(request, "adminindex.html")
            else:
                flag=Registration.objects.filter(Q(email=emailid) & Q(password=pwd))
                if flag:
                    user=Registration.objects.get(email=emailid)
                    request.session["uname"]=user.fullname
                    request.session["uemail"]=user.email
                    return render(request,"customerindex.html",{"uname":user.fullname,"uemail":user.email})
                else:
                    msg = "Invalid Login!"
                    return render(request,"login.html",{"msg":msg})


def viewusers(request):
    usersdata = Registration.objects.all()
    userscount = Registration.objects.count()
    return render(request,"viewusers.html",{"users":usersdata,"count":userscount})

def deleteuser(request,uid):
    Registration.objects.filter(id=uid).delete()
    return redirect("viewusers")

def customerfunction(request):
    uname = request.session["uname"]
    uemail = request.session["uemail"]
    return render(request,"customerindex.html",{"uname":uname,"uemail":uemail})

def bookcaruser(request):
    uname = request.session["uname"]
    uemail = request.session["uemail"]
    return render(request,"bookcaruser.html",{"uname":uname,"uemail":uemail})

def changepassword(request):
    uname = request.session["uname"]
    uemail = request.session["uemail"]
    return render(request,"changepassword.html",{"uname":uname,"uemail":uemail})

def updatepassword(request):
    uemail = request.session["uemail"]
    if request.method == "POST":
        opsw = request.POST["cpsw"]
        npsw = request.POST["npsw"]
        rpsw = request.POST["rpsw"]
        flag = Registration.objects.filter(Q(email=uemail) & Q(password=opsw))
        if flag:
            if npsw == rpsw:
                if (len(npsw) >= 8):
                    if (bool(re.match('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,30})', npsw)) == True):
                        msg = "Old password changed Successful !!"
                        Registration.objects.filter(email=uemail).update(password=npsw)
                        return render(request, "changepassword.html", {"msg": msg})
                    else:
                        msg = "Password must contain atleast one number [0-9],uppercase [A-Z],special character [!@#$%^&*]!! try again!!"
                        return render(request, "changepassword.html", {"msg": msg})
                else:
                    msg = " Password Length should be >=8 !! try again!!"
                    return render(request, "changepassword.html", {"msg": msg})
            else:
                msg = 'Password and Confirm Password Does Not Match !! try again!!'
                return render(request, "changepassword.html", {"msg": msg})

        else:
            msg = "Old password is incorrect!"
            return render(request, "changepassword.html", {"msg": msg})

def bookcaruser(request):
    return redirect("viewcars")

def addcar(request):
    if request.method == 'POST':
        msg="Added Successfully"
        form = CarsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "addcar.html",{"msg": msg,"form":form})
    else:
        form = CarsForm()
    return render(request, "addcar.html", {"form": form})
def customerfunction(request):
    uname = request.session["uname"]
    return render(request,"customerindex.html",{"uname":uname})

def viewcars(request):
    carsdata = CarModels.objects.all()
    #userscount = Registration.objects.count()
    return render(request,"viewcars.html",{"car":carsdata})

def bookcarpage(request):
    return render(request,"bookcar.html")

def viewcarsinhome(request):
    carsdata = CarModels.objects.all()
    #userscount = Registration.objects.count()
    return render(request,"bookcar.html",{"car":carsdata})

def viewcarsinadmin(request):
    carsdata = CarModels.objects.all()
    #userscount = Registration.objects.count()
    return render(request,"removecar.html",{"car":carsdata})

def removecar(request,uid):
    CarModels.objects.filter(id=uid).delete()
    return redirect("viewcarsinadmin")

def getcar(request,uid):
    carsdata = CarModels.objects.get(id=uid)
    uemail = request.session["uemail"]
    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        car = CarModels.objects.get(id=uid)
        user = Registration.objects.get(email=uemail)
        contact = request.POST.get('contact')
        pickuptime = request.POST.get('time')
        start_date = datetime.strptime(checkin, '%Y-%m-%d')
        end_date = datetime.strptime(checkout, '%Y-%m-%d')
        delta = end_date - start_date
        num_days = delta.days+1
        carprice = car.price
        tprice = carprice*num_days
        if not check_booking(checkin, checkout, uid):
            msg = "Car is already booked in these dates"
            return render(request, "demo.html", {"msg": msg, "car": carsdata})
        CarBooking.objects.create(car=car, user=user, startdate=checkin, enddate=checkout,contact=contact,pickuptime=pickuptime,tprice=tprice)
        msg = "Your booking has been saved"
        return render(request, 'demo2.html', {"msg": msg,'num_days': num_days,"car": carsdata})
    return render(request,"demo.html",{"car":carsdata})

def check_booking(startdate, enddate, id):
    qs = CarBooking.objects.filter(
        startdate__lte=enddate,
        enddate__gte=startdate,
        car__id=id
    )
    if len(qs) >= 1:
        return False
    return True

def proceedtopay(request):
    return render(request, 'demo2.html')


def paymentsuccess(request):
    payment_id = request.GET.get('payment_id')
    context = {'payment_id': payment_id}
    return render(request,"paymentsuccess.html",context)


def downloadfile(request):
    template_path = 'paymentsuccess.html'
    payment_id = request.GET.get('payment_id')
    context = {'payment_id': payment_id, 'download': True}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="payment_success.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa.CreatePDF(html, dest=response)

    return response

def viewbookings(request):
    usersdata = CarBooking.objects.all()
    userscount = CarBooking.objects.count()
    return render(request,"viewbooking.html",{"users":usersdata,"count":userscount})


def contact(request):
    form=ContactForm()

    if request.method == "POST":
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
            msg="Query Submitted Successfully"
            return render(request,"contactpage.html",{"msg":msg,"form":form})
        else:
            msg="Failed to Submit Query !"
            return render(request, "contactpage.html", {"msg": msg,"form":form})

    return render(request,"contactpage.html",{"form":form})


def viewquery(request):
    userdata = Contact.objects.all()
    return render(request,"viewquery.html",{"users":userdata})



