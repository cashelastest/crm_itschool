# Generated by Django 5.1.2 on 2024-10-28 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0009_remove_student_paid_pack_student_paid_pack'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='paid_pack',
            field=models.ManyToManyField(blank=True, null=True, to='school.pack', verbose_name='Оплачений пакет'),
        ),
    ]
