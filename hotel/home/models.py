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
    hotel_name = models.CharField(max_length=100)
    hotel_price = models.IntegerField()
    description = models.TextField(max_length=500)
    amenities = models.ManyToManyField(Amenities)
    room_count = models.IntegerField(default=10)


    def __str__(self) -> str:
        return self.hotel_name


class HotelImages(BaseModel):
    hotel= models.ForeignKey(Hotel ,related_name="images", on_delete=models.CASCADE)
    images = models.ImageField(upload_to="hotels")



class Booking(BaseModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    start_date = models.DateField()
    end_date = models.DateField()
