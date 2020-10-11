from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class GlobalVariable(models.Model):
    week = models.IntegerField(default=0)
    is_drawn = models.BooleanField(default=False)


class Lab(models.Model):
    week = models.IntegerField(default=0)
    lab_name = models.CharField(max_length=100)
    lab_place = models.CharField(max_length=30)
    lab_capacity = models.IntegerField(default=0)


class LabItem(models.Model):
    lab_time = models.IntegerField(default=0)
    is_available = models.BooleanField(default=False)
    remaining_capacity = models.IntegerField(default=0)
    willing_user = models.ManyToManyField(User, related_name='willing')
    selected_user = models.ManyToManyField(User, related_name='selected')
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)

    def course_id(self):
        return self.lab.pk * 100 + self.lab_time

    def weekday(self):
        return self.lab_time // 10

    def time(self):
        t = self.lab_time % 10
        if t == 1:
            return '上午'
        elif t == 2:
            return '下午'
        else:
            return '晚上'


    class Meta:
        ordering = ['lab_time']


class WaitingListUser(models.Model):
    lab_item = models.ForeignKey(LabItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_in_waiting_list = models.IntegerField(default=0)

    class Meta:
        ordering = ['order_in_waiting_list']
