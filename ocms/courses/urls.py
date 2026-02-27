from django.urls import path
from .views import *
urlpatterns = [
    path('categories/', category_list),
    path('categories/<int:id>/', category_detail),
    path('courses/', course_list),
    path('courses/<int:id>/', course_detail),
    path('courses/<int:id>/full/', course_detail_full),
    path('courses/<int:id>/enroll/', course_enroll),
    path('courses/<int:id>/review/', course_add_review),
    path('modules/', module_list),
    path('modules/<int:id>/', module_detail),
    path('lectures/', lecture_list),
    path('lectures/<int:id>/', lecture_detail),
]