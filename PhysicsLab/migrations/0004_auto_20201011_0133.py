# Generated by Django 3.1.2 on 2020-10-11 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhysicsLab', '0003_auto_20201008_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='labitem',
            name='lab_week',
        ),
        migrations.AddField(
            model_name='lab',
            name='week',
            field=models.IntegerField(default=0),
        ),
    ]