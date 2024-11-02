# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class SchoolCourse(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'school_course'


class SchoolLesson(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    homework = models.TextField()
    ispayed = models.BooleanField(db_column='isPayed')  # Field name made lowercase.
    isconfirmed = models.BooleanField(db_column='isConfirmed')  # Field name made lowercase.
    course = models.ForeignKey(SchoolCourse, models.DO_NOTHING)
    student = models.ForeignKey('SchoolStudent', models.DO_NOTHING)
    teacher = models.ForeignKey('SchoolTeacher', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'school_lesson'


class SchoolPack(models.Model):
    name = models.CharField(max_length=255)
    lessons_number = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    validity_period = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'school_pack'


class SchoolProfile(models.Model):
    role = models.CharField(max_length=10)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'school_profile'


class SchoolSchedule(models.Model):
    day_of_week = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    pack = models.ForeignKey(SchoolPack, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'school_schedule'


class SchoolStudent(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)
    paid_pack = models.ForeignKey(SchoolPack, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'school_student'


class SchoolTeacher(models.Model):
    salary_per_hour = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    balance = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    paid = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'school_teacher'


class SchoolTeacherCourses(models.Model):
    teacher = models.ForeignKey(SchoolTeacher, models.DO_NOTHING)
    course = models.ForeignKey(SchoolCourse, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'school_teacher_courses'
        unique_together = (('teacher', 'course'),)
