# Generated by Django 3.0 on 2021-04-06 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0036_student_request_fees_master'),
    ]

    operations = [
        migrations.AddField(
            model_name='content_by_student',
            name='date',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
