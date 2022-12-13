from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView, DeleteView
from phone_field import phone_number
from .models import (Amenities, Hotel, Booking)
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth import logout
from . import models

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
            if checkin > timezone.now().date():
                messages.warning(request, 'Отель уже забронирован на эти даты ')
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

def booking(request):

    return render(request, 'booking.html',)

class booking(TemplateView):

    def get(self,request):

         bookings = Booking.objects.all()          # worth looking into?

         return render(request, 'booking.html', {'bookings': bookings})

class BookingDelete(DeleteView):
    model = models.Booking
    template_name = ''
    success_url = reverse_lazy('home')