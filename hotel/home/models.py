from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import uuid

from phone_field import PhoneField


class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4   , editable=False , primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Amenities(BaseModel):
    amenity_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.amenity_name

class Hotel(BaseModel):
    hotel_name = models.CharField(max_length=100, verbose_name = "Название номера")
    hotel_price = models.IntegerField(verbose_name = "Цена номера")
    description = models.TextField(max_length=500, verbose_name = "Описание")
    amenities = models.ManyToManyField(Amenities, verbose_name = "Удобства номера")
    room_count = models.IntegerField(default=1, verbose_name = "Количество бронирований")
    people_capacity = models.IntegerField(default=0, verbose_name = "Вместимость")

    def __str__(self) -> str:
        return self.hotel_name


class HotelImages(BaseModel):
    hotel= models.ForeignKey(Hotel ,related_name="images", on_delete=models.CASCADE, verbose_name = "Название номера")
    images = models.ImageField(upload_to="hotels", verbose_name = "Изображение")



class Booking(BaseModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    start_date = models.DateField()
    end_date = models.DateField()
