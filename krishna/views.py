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
# User here
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.db.models import Q
from datetime import datetime,date

# Create your views here.
def Home(request):
    room_types_queryset = Rooms.objects.values('room_type').distinct()
    room_types = RoomType.objects.all()
    rooms = Rooms.objects.all()
    reservation = Reservation.objects.all()
    if request.user.id != None:
        userprofile = UserProfile.objects.get(user_id=request.user.id)
        return render(request, 'user/homeUser.html', {'roomtype': room_types, 'rooms': rooms,'reservation':reservation,'userprofile':userprofile})
    else :
        return render(request, 'user/homeUser.html', {'roomtype': room_types,'reservation':reservation, 'rooms': rooms})

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


#staff panel page
def panel(request):

    if request.user.is_staff == True:  
        rooms = Rooms.objects.all()
        total_rooms = len(rooms)
        available_rooms = len(Rooms.objects.all().filter(status='1'))
        unavailable_rooms = len(Rooms.objects.all().filter(status='2'))
        reserved = len(Reservation.objects.all())

        hotel = Hotels.objects.values_list('location','id').distinct().order_by()

        response = render(request,'staff/panel.html',{'location':hotel,'reserved':reserved,'rooms':rooms,'total_rooms':total_rooms,'available':available_rooms,'unavailable':unavailable_rooms})
        return HttpResponse(response)
    else:
        return HttpResponse('Access Denied')

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


# --------------------------------------------------------------------------------
# User here
def Userlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)
        
        if user is not None:
            if not user.is_staff:
                login(request, user)
                messages.success(request, "Đăng nhập thành công") 
                return redirect('homeUser')
            else:
                login(request, user)
                return redirect('staffpanel')
        else:
            messages.error(request, "Sai tài khoản hoặc mật khẩu.")
            return redirect('homeUser')

def Userlogout(request):
    if request.method =='GET':
        logout(request)
        return redirect('homeUser')
    else:
        print("logout unsuccessfull")
        return redirect('homeUser')
def Usersignin(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        username = User.objects.get(username = username)
        if username == None:
            messages.success(request,"Tài khoản đã tồn tại")
        else :
            new_user = User.objects.create_user(username=username,password=password)
            new_user.is_superuser=False
            new_user.is_staff=False
            new_user.save()
            messages.success(request,"Đăng kí thành công")
            return redirect('homeUser')
    else:
        print("logout unsuccessfull")
        return redirect('homeUser')
def SearchRoom(request):
    if request.method == 'POST':
        checkin_str = request.POST.get('check_in')
        checkout_str = request.POST.get('check_out')
        reservation = Reservation.objects.all()

        checkin = datetime.strptime(checkin_str, '%m/%d/%Y').strftime('%Y-%m-%d')
        checkout = datetime.strptime(checkout_str, '%m/%d/%Y').strftime('%Y-%m-%d')

        roomtype = request.POST.get('roomtype')
        location = request.POST.get('location')
        
        rooms_in_location = Rooms.objects.filter(hotel__country=location, room_type__type_name=roomtype)
        
        reservations_in_range = Reservation.objects.filter(
            Q(check_in__range=(checkin, checkout)) | Q(check_out__range=(checkin, checkout))
        )
        
        reserved_rooms = [reservation.room for reservation in reservations_in_range]
        
        available_rooms = rooms_in_location.exclude(id__in=[room.id for room in reserved_rooms])
        
     
        return render(request,'user/roomSearch.html', {'room': available_rooms,'reservation':reservation,'checkin':checkin,'checkout':checkout})
def RoomTypePage(request,roomtype):
    if request.method == 'GET':
        roomtypes = RoomType.objects.get(id=roomtype)
        rooms = Rooms.objects.filter(room_type=roomtypes)
        print ("Room type",roomtypes)
        reservations = Reservation.objects.filter(room__room_type=roomtypes)
        return render(request, 'user/roomType.html', {'roomtypes': roomtypes, 'rooms': rooms,'reservation':reservations})
    
def send_email(title, html_content, email_receive):
    email_send = 'nhataaghjkl@gmail.com'
    password = 'yyfa bbsv xsmj oeyu'
    email_to = email_receive
    message = MIMEMultipart()
    message['From'] = email_send
    message['To'] = email_to
    message['Subject'] = title
    content = MIMEText(html_content, 'html') 
    message.attach(content)
    with smtplib.SMTP('smtp.gmail.com', 587) as session:
        session.starttls()
        session.login(email_send, password)
        session.sendmail(email_send, email_to, message.as_string())

def AddReservation(request):
    if request.method == 'POST':
        guest_id = request.POST['guest_id']
        room_id = request.POST['room_id']
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']

        user = User.objects.get(id =guest_id)
        room = Rooms.objects.get(id = room_id)

        html_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Confirmation Email - Hotel Reservation</title>
                <style>
                    /* Style cho email */
                    body {
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                    }
                    .container {
                        max-width: 600px;
                        margin: auto;
                        padding: 20px;
                        border: 1px solid #ccc;
                        border-radius: 10px;
                    }
                    h2 {
                        color: #333;
                    }
                    p {
                        margin-bottom: 20px;
                    }
                    .button {
                        display: inline-block;
                        background-color: #007bff;
                        color: #fff;
                        text-decoration: none;
                        padding: 10px 20px;
                        border-radius: 5px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Xác nhận Đặt phòng Khách sạn</h2>
                    <p>Xin chào """+user.first_name+"""</p>
                    <p>Cảm ơn bạn đã đặt phòng tại khách sạn """+room.hotel.name+""". Dưới đây là thông tin về đặt phòng của bạn:</p>
                    <ul>
                        <li><strong>Ngày Nhận Phòng:</strong> """+check_in+"""</li>
                        <li><strong>Ngày Trả Phòng:</strong> """+check_out+"""</li>
                        <li><strong>Địa chỉ :</strong> """+room.hotel.location +""" - """+ room.hotel.country+"""</li>
                         <li><strong>Mã Số Phòng:</strong> """+str(room.roomnumber)+"""</li>
                        
                    </ul>
                    <p>Vui lòng kiểm tra lại thông tin và liên hệ với chúng tôi nếu có bất kỳ thắc mắc nào.</p>
                    <p>Xin cảm ơn!</p>
                    <p>Trân trọng,<br>Đội ngũ Khách sạn """+room.hotel.name+"""</p>
                    <a href="" class="button">Trang Chủ</a>
                </div>
            </body>
            </html>

        """

        send_email('Đặt phòng khách sạn',html_content ,user.email)
        profile = UserProfile.objects.get(user = user)

        if user.email == '' or profile.sdt == '':
            messages.success(request,"Đặt phòng thất bại . Kiểm tra thông tin cá nhân.", extra_tags='logoutsuccess')
            return redirect(request,'homeUser')
        else :
            newreservation = Reservation()
            newreservation.guest_id = guest_id
            newreservation.room_id = room_id
            newreservation.check_in = check_in
            newreservation.check_out = check_out
            newreservation.save()
            messages.success(request,"Đặt phòng thành công", extra_tags='logoutsuccess')

            return redirect('homeUser')

    else:
        messages.success(request,"Đặt phòng thất bại", extra_tags='logoutsuccess')
        return redirect('homeUser')
def SearchRoom(request):
    if request.method == 'POST':
        checkin_str = request.POST.get('check_in')
        checkout_str = request.POST.get('check_out')
        reservation = Reservation.objects.all()

        checkin = datetime.strptime(checkin_str, '%m/%d/%Y').strftime('%Y-%m-%d')
        checkout = datetime.strptime(checkout_str, '%m/%d/%Y').strftime('%Y-%m-%d')

        roomtype = request.POST.get('roomtype')
        location = request.POST.get('location')
        
        rooms_in_location = Rooms.objects.filter(hotel__country=location, room_type__type_name=roomtype)
        
        reservations_in_range = Reservation.objects.filter(
            Q(check_in__range=(checkin, checkout)) | Q(check_out__range=(checkin, checkout))
        )
        
        reserved_rooms = [reservation.room for reservation in reservations_in_range]
        
        available_rooms = rooms_in_location.exclude(id__in=[room.id for room in reserved_rooms])
        
        return render(request,'user/roomSearch.html', {'room': available_rooms,'reservation':reservation,'checkin':checkin,'checkout':checkout})
    

def RoomBooking(request):
    reservation = Reservation.objects.filter(guest__id=request.user.id)
    userprofile = UserProfile.objects.get(user_id=request.user.id)

    datenow = datetime.now()
    return render(request,'user/roomBooking.html',{'reservation':reservation,'userprofile':userprofile,'datenow':datenow})

def CancelReservation(request,rsId):
    res = get_object_or_404(Reservation, id=rsId)
    res.delete()
    messages.success(request,"Hủy phòng thành công")
    return redirect('roombooking')

def Profile(request):
    user_profile = UserProfile.objects.all()
    for profile in user_profile:
        if profile.user.id == request.user.id:
            userprofile = profile
            break
    roomUser = Reservation.objects.filter(guest_id=request.user.id).order_by('check_in')
    return render(request, 'user/profileUser.html', {'userprofile': userprofile, 'roomUser': roomUser})

def UpdateProfile(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        user = User.objects.filter(id=user_id).first()
        userprofile = UserProfile.objects.get(user_id=user_id)
        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            userprofile.address = address
            userprofile.sdt = phone
            userprofile.save()
            return redirect('profileUser')
        else:
            pass

def image_to_base64(image):
    encoded_string = base64.b64encode(image.read())
    return encoded_string.decode('utf-8')

def UploadAvata(request):
    if request.method == 'POST':
        uploaded_image = request.FILES['newavata']  
        base64_image = image_to_base64(uploaded_image)
        user_profile = UserProfile.objects.all()
        for profile in user_profile:
            if profile.user.id == request.user.id:
                userprofile = profile
                break
        userprofile.avatar = base64_image
        userprofile.save()
        return redirect('profileUser')

