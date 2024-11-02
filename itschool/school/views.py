from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from .models import Lesson
from django.views.generic.edit import CreateView
from .forms import *
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from datetime import datetime,timedelta
from django.views.generic import *
from django.views.decorators.csrf import csrf_exempt
import json
def change_color(lesson):
    if lesson.isConfirmed:
        color = 'black'
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
        print(lesson.start_time)
        end = datetime.combine(lesson.date, lesson.end_time)
        
        events.append({
            'id':f"{lesson.id}",
            'title': f"{lesson.name}",
            'start': start.isoformat(),
            'end': end.isoformat(),
            'teacher':f"{lesson.teacher.user.first_name} {lesson.teacher.user.last_name}",
            'student':f"{lesson.student.user.first_name} {lesson.student.user.last_name}",
            'isConfirmed':f"{lesson.isConfirmed}",
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

@csrf_exempt
def add_pack(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            form_data = body.get('data', {})
            
            print(f"Received form data: {form_data}")
            
            # Проверяем существование курса
            try:
                course = Course.objects.get(id=int(form_data['course']))
                if not hasattr(course, 'teacher') or not course.teacher:
                    raise ValueError("Course has no assigned teacher")
            except Course.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Course with id {form_data["course"]} not found'
                }, status=404)
            
            days = int(form_data['validityPeriod'])
            
            # Конвертируем строки времени в объекты time
            def parse_time(time_str):
                return datetime.strptime(time_str, '%H:%M').time()
            
            # Создаем пакет
            pack = Pack.objects.create(
                name=form_data['name'],
                lessons_number=int(form_data['lessonsNumber']),
                validity_period=days,
                price=float(form_data['price']),
                course=course
            )
            
            for schedule in form_data['schedules']:
                # Парсим время
                start_time = parse_time(schedule['startTime'])
                end_time = parse_time(schedule['endTime'])
                
                # Создаем расписание
                Schedule.objects.create(
                    pack=pack,
                    day_of_week=int(schedule['dayOfWeek']),
                    start_time=start_time,
                    end_time=end_time
                )
                
                # Получаем даты для уроков
            return JsonResponse({
                'status': 'success',
                'message': 'Package successfully created',
                'pack_id': pack.id
            })
            
        except ValueError as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Value error: {str(e)}'
            }, status=400)
            

    courses = Course.objects.all()
    return render(request, 'school/add_pack.html', {'courses': courses})

class payPack(DetailView):
    model = Student
    template_name = "school/student_info.html"
    context_object_name = 'student'
    slug_url_kwarg = 'slug'  # имя параметра в URL
    success_url = 'lessons'
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['student'] = get_object_or_404(Student, slug=self.kwargs['slug'])
        data['packs'] = Pack.objects.all()
        return data
    def get_object(self, queryset=None):

        return get_object_or_404(Student, slug=self.kwargs['slug'])
    
    def post(self, request, *args,**kwargs):
        pack = request.POST.get('pack')
        print(f"{pack}")
        pack = get_object_or_404(Pack, pk = pack)
        student = get_object_or_404(Student, slug=self.kwargs['slug'])
        if pack and student:
            generate_lessons(pack,student)
            return redirect('lessons') 

        else:
            return reverse_lazy('student_info')
@csrf_exempt
def confirmation(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            id = data.get('data')
            lesson = Lesson.objects.get(id=id)
            lesson.isConfirmed = True
            print(lesson)
            lesson.save()
            redirect('home')
            return JsonResponse({'redirect': '/'})
        except (Lesson.DoesNotExist, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid request'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


            #to utils 
def generate_lessons(pack,student):
    schedules = Schedule.objects.filter(pack = pack)
    student.paid_pack.add(pack)
    student.save()

    for schedule in schedules:
        dates = get_lesson_dates(int(schedule.day_of_week),int(pack.validity_period), pack.lessons_number)
        for date in dates:
            Lesson.objects.create(
                        name=pack.name + f'\nЗаняття номер: {dates.index(date) + 1}',
                        date=date,
                        start_time=schedule.start_time,
                        end_time=schedule.end_time,
                        homework='',
                        student = student,
                        teacher=pack.course.teacher,
                        course=pack.course,
                        isPayed=True,
                        isConfirmed=False
                    )
def get_lesson_dates(weekday,day,lessons_num):
    # weekday: 0 - понедельник, 1 - вторник, 2 - среда, и т.д.
    start_date = datetime.now()
    end_date = start_date + timedelta(days=day)
    dates = []
    
    current_date = start_date
    while current_date <= end_date and len(dates) < lessons_num:
        if current_date.weekday() == weekday:  # проверяем нужный день недели
            dates.append(current_date.date())
            print(current_date.date())
        current_date += timedelta(days=1)
    
    return dates