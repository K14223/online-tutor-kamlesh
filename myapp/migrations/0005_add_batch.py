# Generated by Django 3.0 on 2021-02-27 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_parent_contact_student_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Add_batch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bnum', models.CharField(max_length=100)),
                ('bname', models.CharField(max_length=100)),
                ('bsubject', models.CharField(max_length=100)),
                ('bdate', models.CharField(max_length=100)),
                ('btime', models.CharField(max_length=100)),
                ('bday', models.CharField(max_length=100)),
                ('bdetail', models.CharField(max_length=100)),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Tutor')),
            ],
        ),
    ]
