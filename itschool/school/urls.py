from django.urls import path
from .views import *
urlpatterns =[
    path('', home,name = 'home'),
    path('api/events/', get_events, name='get_events'),
    path('lessons/', Show_lessons.as_view(),name='lessons'),
    path('add-lesson/', AddLesson.as_view(), name = 'add_lesson'),
    # path('add-teacher/', AddTeacher.as_view(),name = 'add_teacher'),
    # path('add-student/', AddStudent.as_view(), name = 'add_student'),
    path('sign-up/', register, name='sign-up')
]