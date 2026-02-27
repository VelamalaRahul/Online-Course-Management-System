from django.urls import path
from .views import *
urlpatterns = [
    path('reviews/', review_list),
    path('reviews/<int:id>/', review_detail),
]