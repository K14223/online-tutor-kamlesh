# Generated by Django 3.0 on 2021-03-23 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0030_auto_20210323_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='fees_master',
            name='tutor_detail',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Tutor_details'),
        ),
    ]
