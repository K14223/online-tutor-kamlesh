# Generated by Django 3.0 on 2021-03-15 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_student_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='tutor',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='myapp.Tutor'),
        ),
    ]
