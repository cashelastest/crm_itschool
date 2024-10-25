from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Lesson
from django.views.generic.edit import CreateView
from .forms import *
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import *
def change_color(lesson):
    if lesson.isConfirmed:
        color = '#167d43'
    elif lesson.isPayed:
        color = 'green'
    else:
        color = "red"
    return color
def get_events(request):
    lessons = Lesson.objects.all()
    events = []
    for lesson in lessons:
        print(lesson)
        start = datetime.combine(lesson.date, lesson.start_time)
        end = datetime.combine(lesson.date, lesson.end_time)
        
        events.append({
            'title': f"{lesson.name}",
            'start': start.isoformat(),
            'end': end.isoformat(),
            'teacher':f"{lesson.teacher.user.username}",
            'homework':f"{lesson.homework}",
            'color':change_color(lesson),
        })
    return JsonResponse(events, safe=False)
class Show_lessons(ListView):
    model = Lesson
    context_object_name = 'lessons'
    template_name = 'school/lessons.html'

def home(request):
    return render(request, 'school/home.html')
# Create your views here.
class AddLesson(CreateView):
    form_class = LessonForm
    model = Lesson
    template_name = 'school/add_lesson.html'
    success_url = reverse_lazy('home')

# class AddTeacher(CreateView):
#     form_class = TeacherForm
#     model = Teacher
#     template_name = 'school/add_teacher.html'
#     success_url = reverse_lazy('lessons')
# class AddStudent(CreateView):
#     form_class = StudentForm
#     model = Student
#     template_name = 'school/add_teacher.html'
#     success_url = reverse_lazy("add_lesson")
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            Profile.objects.create(user=user, role=role)

            if role == 'student':
                Student.objects.create(
                    user=user,
                    balance=0,
                    paid_pack=None  # Нужно будет добавить логику выбора пакета
                )
            elif role == 'teacher':
                Teacher.objects.create(
                    user=user,
                    salary_per_hour=0,
                    balance=0
                )
            login(request, user)
            messages.success(request, 'Реєстрація успішна!')
            return redirect('home')  
        else:
            messages.error(request, 'Помилка реєстрації. Перевірте дані.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'school/add_lesson.html', {'form': form})