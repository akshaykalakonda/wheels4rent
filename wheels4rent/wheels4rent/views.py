import razorpay
from django.http import HttpResponse
from django.shortcuts import render


from django.shortcuts import render


def homepage(request):
    return render(request,"index.html")

def loginpage(request):
    return render(request,"login.html")

def aboutpage(request):
    return render(request,"about.html")

def registrationpage(request):
    return render(request,"registration.html")




