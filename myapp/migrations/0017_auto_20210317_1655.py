# Generated by Django 3.0 on 2021-03-17 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_attendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='astatus',
            field=models.CharField(default='Absent', max_length=100),
        ),
    ]