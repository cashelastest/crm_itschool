from django import forms
from .models import Pack, Course, Student, Teacher, Profile, Lesson

from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile 
class CustomFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-input'
            })

class UserRegistrationForm(CustomFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PackForm(CustomFormMixin, forms.ModelForm):
    class Meta:
        model = Pack
        fields = ['name', 'lessons_number', 'price']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Введіть назву пакету'
            }),
            'lessons_number': forms.NumberInput(attrs={
                'min': '1'
            }),
            'price': forms.NumberInput(attrs={
                'min': '0',
                'step': '0.01'
            })
        }

class CourseForm(CustomFormMixin, forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-textarea'
            })
        }

class StudentForm(CustomFormMixin, forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user','balance', 'paid_pack']
        widgets = {
            'balance': forms.NumberInput(attrs={
                'min': '0',
                'step': '0.01'
            }),
            'paid_pack': forms.Select(attrs={
                'class': 'form-select'
            })
        }

class TeacherForm(CustomFormMixin, forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['user','salary_per_hour', 'courses']
        widgets = {
            'salary_per_hour': forms.NumberInput(attrs={
                'min': '0',
                'step': '10.0'
            }),
            'courses': forms.SelectMultiple(attrs={
                'class': 'form-multiselect'
            })
        }

class ProfileForm(CustomFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={
                'class': 'form-select'
            })
        }

class LessonForm(CustomFormMixin, forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name', 'date', 'start_time', 'end_time', 'homework', 'teacher', 'student', 'course']
        widgets = {
            'name': forms.TextInput(),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-input'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-input'
            }),
            'homework': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-textarea'
            }),
            'teacher': forms.Select(attrs={
                'class': 'form-select'
            }),
            'student': forms.Select(attrs={
                'class': 'form-select'
            }),
            'course': forms.Select(attrs={
                'class': 'form-select'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError(
                "Час початку уроку повинен бути раніше часу закінчення"
            )
        
        return cleaned_data
    
class UserRegistrationForm(CustomFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, label="Ім'я")
    last_name = forms.CharField(required=True, label="Прізвище")
    role = forms.ChoiceField(
        choices=Profile.ROLES, 
        label="Роль",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None