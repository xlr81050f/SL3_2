from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('books/',views.bookt,name="books"),
    path('delete/',views.delete,name="delete"),
    path('delete/delt/',views.delt,name="delt"),
    path('updatetime/',views.updatetime,name="updatetime"),
    path('details/',views.details,name="details"),
    path('viewticket/',views.viewticket,name="viewticket"),
    path('viewticket/viewticketfn/',views.viewticketfn,name="viewticketfn"),
    path('details/userdetailsfn',views.userdetailsfn,name="userdetails"),
    path('updatetime/updatetimefn',views.updatetimefn,name="updatetime"),
    
]