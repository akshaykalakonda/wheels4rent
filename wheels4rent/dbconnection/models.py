from django.db import models

# Create your models here.
class Registration(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False, unique=True)
    password = models.CharField(max_length=100, blank=False)
    contact = models.BigIntegerField(blank=False, unique=True)
    registrationtime = models.DateTimeField(blank=False, auto_now=True)

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = "registration_table"




class CarModels(models.Model):
    id = models.AutoField(primary_key=True)
    carname = models.CharField(max_length=100, blank=False)
    carmodel = models.CharField(max_length=50,blank=False)
    price = models.BigIntegerField(blank=False)
    image = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.carname


    class Meta:
        db_table = "car_models"

class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    email=models.CharField(max_length=50,unique=True,blank=False)
    password = models.CharField(max_length=50,blank=False)

    def __str__(self):
        return self.email
    class Meta:
        db_table = "admin_table"



class CarBooking(models.Model):
    car=models.ForeignKey(CarModels,on_delete=models.CASCADE)
    user=models.ForeignKey(Registration,on_delete=models.CASCADE)
    startdate=models.DateField()
    enddate=models.DateField()
    contact = models.BigIntegerField(blank=False,default=False,unique=False)
    pickuptime = models.CharField(max_length=50, blank=False,default=False)
    tprice = models.BigIntegerField(blank=False,default=None)

    class Meta:
        db_table = "booking_table"


class Contact(models.Model):

    email=models.CharField(max_length=50,unique=True,blank=False)
    user = models.CharField(max_length=50,unique=True,blank=False)
    message=models.TextField()
    class Meta:
        db_table = "contact_table"