from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView, CreateView, UpdateView
from phone_field import phone_number
from .models import (Amenities, Hotel, Booking, HotelImages)
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth import logout
from .forms import *
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

def check_booking(start_date  , end_date ,uid , room_count):
    qs = Booking.objects.filter(
        start_date__lte=start_date,
        end_date__gte=end_date,
        hotel__uid = uid
        )
    
    if len(qs) >= room_count:
        return False
    
    return True
    
def home(request):
    amenities_objs = Amenities.objects.all()
    hotels_objs = Hotel.objects.all()


    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    amenities = request.GET.getlist('amenities')
    print(amenities)
    if sort_by:
        if sort_by == 'ASC':
            hotels_objs = hotels_objs.order_by('hotel_price')
        elif sort_by == 'DSC':
            hotels_objs = hotels_objs.order_by('-hotel_price')

    if search:
        hotels_objs = hotels_objs.filter(
            Q(hotel_name__icontains = search) |
            Q(description__icontains = search) )


    if len(amenities):
        hotels_objs = hotels_objs.filter(amenities__amenity_name__in = amenities).distinct()



    context = {'amenities_objs' : amenities_objs , 'hotels_objs' : hotels_objs , 'sort_by' : sort_by 
    , 'search' : search , 'amenities' : amenities}
    return render(request , 'home.html' ,context)



def hotel_detail(request,uid):
    hotel_obj = Hotel.objects.get(uid = uid)

    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout= request.POST.get('checkout')
        phone = request.POST.get('phone_0')
        hotel = Hotel.objects.get(uid = uid)
        if not check_booking(checkin ,checkout,  uid , hotel.room_count):
            messages.warning(request, 'Номер уже забронирован на эти даты ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        Booking.objects.create(hotel=hotel ,phone=phone, user = request.user , start_date=checkin
        , end_date = checkout , )
        
        messages.success(request, 'Ваше бронирование сохранено')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

        
    
    return render(request , 'hotel_detail.html' ,{
        'hotels_obj' :hotel_obj
    })


def logout_request(request):
	logout(request)
	messages.info(request, "Вы успешно вышли из аккаунта.")
	return redirect('home')


def aboutpage(request):
    return render(request, 'about_page.html',)


class booking(TemplateView):

    def get(self,request):

         bookings = Booking.objects.all()

         return render(request, 'booking.html', {'bookings': bookings})

def delete_bookings(request, uid):
    bookings = Booking.objects.get(uid=uid)
    bookings.delete()
    return redirect('booking')

def delete_hotel(request, uid):
    hotel_obj = Hotel.objects.get(uid = uid)
    hotel_obj.delete()
    return redirect('home')

class newhotel(CreateView):
    model = Hotel
    fields = ['hotel_name','hotel_price','description','amenities','room_count','people_capacity']
    template_name = 'newhotel.html'
    success_url = reverse_lazy('home')
    def form_valid(self,form):
        # currentUser = self.request.user.owner
        # hotel = Hotel.objects.filter(admin=currentUser.pk).all()
        return super().form_valid(form)

class galleryadd(CreateView):
    model = HotelImages
    fields = ['hotel','images',]
    template_name = 'addphoto.html'
    success_url = reverse_lazy('home')
    def form_valid(self,form):
        # currentUser = self.request.user.owner
        # hotel = Hotel.objects.filter(admin=currentUser.pk).all()
        return super().form_valid(form)

def edit_hotel(request, uid):
    if request.method=="POST":
        instance = Hotel.objects.get(uid = uid)
        form =HotelForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            hotel = form.save(commit = False)
            hotel.save()
        return redirect('home')
    elif Hotel.objects.get(uid = uid):
        hotel = Hotel.objects.get(uid = uid)
        form = HotelForm(instance=hotel)
    else:
        form = HotelForm()
    return render(request,'edithotel.html',{"form":form})