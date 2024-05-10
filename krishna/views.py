from django.shortcuts import render ,redirect
from django.http import HttpResponse , HttpResponseRedirect
from .models import Hotels,Rooms,Reservation, UserProfile, RoomType 
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
from django.shortcuts import redirect, get_object_or_404


# Create your views here.
def homepage(request):
    return render(request, 'staff/homepage.html')
#about
def aboutpage(request):
    return HttpResponse(render(request,'about.html'))

#contact page
def contactpage(request):
    return HttpResponse(render(request,'contact.html'))

#staff sign up
def staff_sign_up(request):
    if request.method =="POST":
        user_name = request.POST['username']
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.success(request,"Password didn't Matched")
            return redirect('staffloginpage')
        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request,"Username Already Exist")
                return redirect("staffloginpage")
        except:
            pass
        
        new_user = User.objects.create_user(username=user_name,password=password1)
        new_user.is_superuser=False
        new_user.is_staff=True
        new_user.save()
        messages.success(request," staff Registration Successfull")
        return redirect("staffloginpage")
    else:

        return HttpResponse('Access Denied')

#staff login and signup page
def staff_log_sign_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                if user.is_staff:
                    login(request, user)
                    return redirect('staffpanel')
                else:
                    messages.error(request, "You are not authorized to access this panel.")
            else:
                messages.error(request, "Your account is currently inactive.")
        else:
            messages.error(request, "Incorrect username or password")
        
        return redirect('staffloginpage')
    
    return render(request, 'staff/stafflogsign.html')
#stafflogoutpage
def logoutuser(request):
    if request.method =='GET':
        logout(request)
        messages.success(request,"Logged out successfully")
        print("Logged out successfully")
        return redirect('userloginpage')
    else:
        print("logout unsuccessfull")
        return redirect('homepage')

#staff panel page
@login_required(login_url='/staff')
def panel(request):
    
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')
    
    rooms = Rooms.objects.all()
    total_rooms = len(rooms)
    available_rooms = len(Rooms.objects.all().filter(status='1'))
    unavailable_rooms = len(Rooms.objects.all().filter(status='2'))
    reserved = len(Reservation.objects.all())

    hotel = Hotels.objects.values_list('location','id').distinct().order_by()

    response = render(request,'staff/panel.html',{'location':hotel,'reserved':reserved,'rooms':rooms,'total_rooms':total_rooms,'available':available_rooms,'unavailable':unavailable_rooms})
    return HttpResponse(response)

#for editing room information
@login_required(login_url='/staff')
def edit_room(request):
    if request.method == 'POST':
        if not request.user.is_staff:
            return HttpResponse('Access Denied')

        room_id = request.POST.get('roomid')
        old_room = Rooms.objects.get(id=int(room_id))

        # Cập nhật thông tin từ form
        old_room.room_type_id = int(request.POST.get('roomtype'))

        if 'image' in request.FILES:
            image_data = request.FILES['image'].read()
            old_room.image = base64.b64encode(image_data).decode('utf-8')

        old_room.capacity = int(request.POST['capacity'])
        old_room.price = int(request.POST['price'])
        old_room.size = int(request.POST['size'])
        old_room.hotel_id = int(request.POST['hotel'])
        old_room.status = request.POST['status']
        old_room.roomnumber = int(request.POST['roomnumber'])
        old_room.description = request.POST['description']

        old_room.save()
        messages.success(request, "Room Details Updated Successfully")
        return redirect('staffpanel')
    else:
        room_id = request.GET.get('roomid')
        room = Rooms.objects.get(id=room_id)
        roomtypes = RoomType.objects.all()
        return render(request, 'staff/editroom.html', {'room': room, 'roomtypes': roomtypes})
    
# Trong views.py
@login_required(login_url='/staff')
def add_room_page(request):
    roomtypes = RoomType.objects.all()
    hotels = Hotels.objects.all()
    return render(request, 'staff/addroom.html', {'roomtypes': roomtypes, 'hotels': hotels})

@login_required(login_url='/staff')
def add_new_room(request):
    if request.method == 'POST':
        if not request.user.is_staff:
            return HttpResponse('Access Denied')
        print("1")
        new_room = Rooms()
        print("2")
        # Cập nhật thông tin từ form
        new_room.room_type_id = int(request.POST.get('roomtype'))
        print("3")
        if 'image' in request.FILES:
            image_data = request.FILES['image'].read()
            new_room.image = base64.b64encode(image_data).decode('utf-8')
        print("4")
        new_room.capacity = int(request.POST['capacity'])
        print("5")
        new_room.price = int(request.POST['price'])
        print("6")
        new_room.size = int(request.POST['size'])
        print("7")
        new_room.hotel_id = int(request.POST['hotel'])
        print("8")
        new_room.status = request.POST['status']
        print("9")
        new_room.roomnumber = int(request.POST['roomnumber'])
        print("10")
        new_room.description = request.POST['description']
        print("11")

        new_room.save()
        messages.success(request, "Room Details Add Successfully")
        return redirect('staffpanel')

def handler404(request):
    return render(request, '404.html', status=404)

@login_required(login_url='/staff')   
def view_room(request):
    room_id = request.GET['roomid']
    room = Rooms.objects.all().get(id=room_id)

    reservation = Reservation.objects.all().filter(room=room)
    return HttpResponse(render(request,'staff/viewroom.html',{'roomr':room,'reservations':reservation}))
@login_required(login_url='/staff')
def delete_room(request):
    room_id = request.GET.get('roomid')
    room = Rooms.objects.all().get(id=room_id)
    room.delete()
    messages.success(request, "Room Deleted Successfully")
    return redirect('staffpanel')

@login_required(login_url='/staff')
def add_new_location(request):
    if request.method == "POST" and request.user.is_staff:
        owner = request.POST['new_owner']
        location = request.POST['new_city']
        state = request.POST['new_state']
        country = request.POST['new_country']
        
        hotels = Hotels.objects.all().filter(location = location , state = state)
        if hotels:
            messages.warning(request,"Sorry City at this Location already exist")
            return redirect("staffpanel")
        else:
            new_hotel = Hotels()
            new_hotel.owner = owner
            new_hotel.location = location
            new_hotel.state = state
            new_hotel.country = country
            new_hotel.save()
            messages.success(request,"New Location Has been Added Successfully")
            return redirect("staffpanel")

    else:
        return HttpResponse("Not Allowed")
    
#for showing all bookings to staff
@login_required(login_url='/staff')
def all_bookings(request):
   
    bookings = Reservation.objects.all()
    if not bookings:
        messages.warning(request,"No Bookings Found")
    return HttpResponse(render(request,'staff/allbookings.html',{'bookings':bookings}))
    
@login_required(login_url='/staff')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Reservation, id=booking_id)
    booking.delete()
    return redirect('allbookigs')  # Assuming 'booking_list' is the name of the URL pattern for the booking list page

@login_required(login_url='/staff')
def all_users(request):
    user_profile = UserProfile.objects.all()
    return render(request, 'staff/all_users.html', {'users': user_profile})

@login_required(login_url='/staff')
def lock_account(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
        # Đặt thông báo hoặc thực hiện bất kỳ hành động nào khác sau khi khóa tài khoản thành công
        return redirect('all_users')  # Điều hướng về trang hiển thị tất cả người dùng
    else:
        return HttpResponse("Không được phép")
@login_required(login_url='/staff')
def unlock_account(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        # Đặt thông báo hoặc thực hiện bất kỳ hành động nào khác sau khi mở khóa tài khoản thành công
        return redirect('all_users')
@login_required(login_url='/staff')
def search_users(request):
    if request.method == 'GET':
        search_query = request.GET.get('search')
        if search_query:
            # Tìm kiếm user theo username hoặc email
            user_profile = UserProfile.objects.filter(Q(user__username__icontains=search_query) | Q(user__email__icontains=search_query))
            return render(request, 'staff/all_users.html', {'users': user_profile})
        else:
            # Hiển thị tất cả users nếu không có truy vấn tìm kiếm
            user_profile = UserProfile.objects.all()
            return render(request, 'staff/all_users.html', {'users': user_profile})
    else:
        return HttpResponse("Not Allowed")


@login_required(login_url='/staff')
def add_roomtype_page(request):
    return render(request, 'staff/addroomtype.html')
@login_required(login_url='/staff')
def add_new_room_type(request):
    if request.method == "POST" and request.user.is_staff:
        type_name = request.POST['room_type']
        description_room_type = request.POST['description']

        # Check if a RoomType with the same type_name already exists
        if RoomType.objects.filter(type_name=type_name).exists():
            messages.error(request, "A Room Type with this name already exists.")
            return redirect('add_roomtype_page')

        new_room_type = RoomType()
        new_room_type.type_name = type_name
        new_room_type.description_room_type = description_room_type
        new_room_type.save()

        messages.success(request, "Room Type Added Successfully")
        return redirect('staffpanel')
    else:
        return HttpResponse("Not Allowed")