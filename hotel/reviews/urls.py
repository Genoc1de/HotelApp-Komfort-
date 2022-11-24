from django.urls import include, path

from . import views
from .views import *

urlpatterns = [
    path('', PostList.as_view(), name='PostList'),
    path('', PostDetail.as_view(), name='PostDetail'),

]




