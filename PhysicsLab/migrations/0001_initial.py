# Generated by Django 3.1 on 2020-10-12 02:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField(default=0)),
                ('is_drawn', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_name', models.CharField(max_length=100)),
                ('lab_place', models.CharField(max_length=30)),
                ('lab_capacity', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LabItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_time', models.IntegerField(default=0)),
                ('is_available', models.BooleanField(default=False)),
                ('remaining_capacity', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['lab_time'],
            },
        ),
        migrations.CreateModel(
            name='WaitingListUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_in_waiting_list', models.IntegerField(default=0)),
                ('lab_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PhysicsLab.labitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['order_in_waiting_list'],
            },
        ),
        migrations.CreateModel(
            name='LabWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField(default=0)),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PhysicsLab.lab')),
            ],
        ),
        migrations.AddField(
            model_name='labitem',
            name='lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PhysicsLab.labweek'),
        ),
        migrations.AddField(
            model_name='labitem',
            name='selected_user',
            field=models.ManyToManyField(related_name='selected', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='labitem',
            name='willing_user',
            field=models.ManyToManyField(related_name='willing', to=settings.AUTH_USER_MODEL),
        ),
    ]
