from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path("save_register", views.save_register, name="save_register"),
    path("customerindex", views.checkuserlogin, name="customerindex"),
    path("viewusers", views.viewusers, name="viewusers"),
    path("deleteuser/<int:uid>", views.deleteuser, name="deleteuser"),
    path("userhome", views.customerfunction, name="userhome"),
    path("changepassword", views.changepassword, name="changepassword"),
    path("updatepassword",views.updatepassword,name="updatepassword"),
    path("bookcaruser", views.bookcaruser, name="bookcaruser"),
    path("addcar", views.addcar, name="addcar"),
    path("viewcars",views.viewcars,name="viewcars"),
    path("bookcar", views.viewcarsinhome, name="bookcar"),
    path("viewcarsinadmin", views.viewcarsinadmin, name="viewcarsinadmin"),
    path("removecar/<int:uid>", views.removecar, name="removecar"),
    path("demo/<int:uid>",views.getcar,name="getcar"),
    path("demo2",views.proceedtopay,name="demo2"),
    path("payment-success", views.paymentsuccess, name="payment-success"),
    path("downloadfile", views.downloadfile, name="downloadfile"),
    path("viewbookings",views.viewbookings,name="viewbookings"),
    path("contact",views.contact,name="contact"),
    path("viewquery",views.viewquery,name="viewquery"),
    path("login",views.test,name="login"),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
