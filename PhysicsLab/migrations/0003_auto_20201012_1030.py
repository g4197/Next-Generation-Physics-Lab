# Generated by Django 3.1 on 2020-10-12 02:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PhysicsLab', '0002_auto_20201012_1024'),
    ]

    operations = [
        migrations.RenameField(
            model_name='labitem',
            old_name='lab',
            new_name='lab_week',
        ),
    ]