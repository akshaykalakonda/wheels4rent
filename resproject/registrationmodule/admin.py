
from django.contrib import admin
from . models import Registration,Admin,CarModels,CarBooking
admin.site.register(Registration)
admin.site.register(CarModels)
admin.site.register(Admin)
admin.site.register(CarBooking)