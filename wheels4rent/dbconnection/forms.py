from django import forms
from captcha.fields import CaptchaField
from django.forms import TextInput, FileInput, ClearableFileInput

from .models import CarModels, Contact


class MyForm(forms.Form):
   captcha=CaptchaField()


class CarsForm(forms.ModelForm):
   class Meta:
        model=CarModels
        fields = "__all__"  # it will display all the fields in the form except default fields like id and registrationtime
       # additional features of the fields
        labels = {"carname": "Enter Car Name",
                "carmodel": "Enter Car Model","price":"Enter Price Per Day","image":"Insert Image"}  # using this, we can change label name in the form
        widgets={'carname': TextInput(attrs={'placeholder': 'Car Name'}),
                  'carmodel': TextInput(attrs={ 'placeholder': 'Car Model'}),
                 'price': TextInput(attrs={'placeholder': 'Price/Day'}),
                  'image': FileInput(attrs={'class': "form-control"}),

                }


class ContactFormEmail(forms.Form):
    fromemail=forms.EmailField(required=True)
    subject=forms.CharField(required=True)
    message=forms.CharField(widget=forms.Textarea,required=True)



class ContactForm(forms.ModelForm):
   class Meta:
        model=Contact
        fields = "__all__"  # it will display all the fields in the form except default fields like id and registrationtime
       # additional features of the fields
        labels = {"email": "Enter Email ID :","user":"Enter Full Name :",
                "message": "Enter Query :"}  # using this, we can change label name in the form
        widgets={'email': TextInput(attrs={'placeholder': 'Email Id'}),
                 'user':TextInput(attrs={'placeholder':'Full Name'}),
                  'message': TextInput(attrs={ 'placeholder': 'Problem Description'})

                }