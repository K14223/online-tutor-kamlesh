# Generated by Django 3.0 on 2021-03-23 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0033_fees_master_tutor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='fees_master',
            name='subject_details',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
