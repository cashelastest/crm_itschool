from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    class Meta:
        # Add this to properly register the model
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
class Pack(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва")
    lessons_number = models.PositiveIntegerField(verbose_name="Кількість уроків")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Ціна")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пакет"
        verbose_name_plural = "Пакети"

class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курси"

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile',verbose_name='Юзер:')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Баланс")
    paid_pack = models.ForeignKey(Pack, on_delete=models.PROTECT, verbose_name="Оплачений пакет", null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенти"

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile', verbose_name='Юзер: ')
    salary_per_hour = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Зарплатня на годину")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Баланс")
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Виплачено")
    courses = models.ManyToManyField(Course, related_name='teachers', verbose_name="Курси")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Викладач"
        verbose_name_plural = "Викладачі"

class Profile(models.Model):
    ROLES = (
        ('student', 'Студент'),
        ('teacher', 'Викладач'),
        ('admin', 'Адміністратор'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, verbose_name="Роль")

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        verbose_name = "Профіль"
        verbose_name_plural = "Профілі"

class Lesson(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва")
    date = models.DateField(verbose_name='Дата уроку', default=date.today)
    start_time = models.TimeField(verbose_name='Час початку')
    end_time = models.TimeField(verbose_name='Час закінчення')
    homework = models.TextField(default='', verbose_name='Домашнє завдання')
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, related_name='lessons', verbose_name="Викладач")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lessons', verbose_name="Студент")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name="Курс")
    isPayed = models.BooleanField(default=False, verbose_name="Оплачено")
    isConfirmed = models.BooleanField(default=False, verbose_name="Підтверджено")

    def __str__(self):
        if self.student.user.first_name or self.student.user.last_name:
            return f"{self.course} - {self.student.user.first_name} {self.student.user.last_name}"
        else:
            return f"{self.course} - {self.student.user.username}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"