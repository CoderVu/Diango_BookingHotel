"""hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import krishna.views as views
urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('about', views.aboutpage,name="aboutpage"),
    path('contact', views.contactpage,name="contactpage"),
    path('staff/', views.staff_log_sign_page,name="staff_log_sign_page"),
    path('staff/login', views.staff_log_sign_page,name="staffloginpage"),
    path('staff/signup', views.staff_sign_up,name="staffsignup"),
    path('logout', views.logoutuser,name="logout"),
    path('staff/panel', views.panel,name="staffpanel"),
    path('staff/allbookings', views.all_bookings,name="allbookigs"),
    path('booking/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('staff/panel/add-new-location', views.add_new_location,name="addnewlocation"),
    path('staff/panel/edit-room', views.edit_room),
    path('staff/panel/add-room/', views.add_room_page, name='add_room_page'),
    path('staff/panel/add-roomtype', views.add_roomtype_page, name='add_roomtype_page'),
    path('staff/panel/add-roomtype/add', views.add_new_room_type, name='add_new_room_type'),
    path('staff/panel/add-new-room', views.add_new_room, name="addroom"),
    path('staff/panel/edit-room/edit', views.edit_room),
    path('staff/panel/delete-room', views.delete_room, name='delete_room'),
    path('staff/panel/view-room', views.view_room),
    path('staff/panel/all_users/', views.all_users, name='all_users'),
    path('staff/panel/all_users/lock-account/', views.lock_account, name='lock_account'),
    path('staff/panel/all_users/unlock-account/', views.unlock_account, name='unlock_account'),
    path('staff/panel/all_user/search_users/', views.search_users, name='search_users'),

    path('admin/', admin.site.urls),
    
    

]
