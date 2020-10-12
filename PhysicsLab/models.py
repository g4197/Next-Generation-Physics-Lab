import random
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class WeekStatus(models.Model):
    week = models.IntegerField(default=0)
    is_drawn = models.BooleanField(default=False)


class Lab(models.Model):
    lab_name = models.CharField(max_length=100)
    lab_place = models.CharField(max_length=30)
    lab_capacity = models.IntegerField(default=0)


class LabWeek(models.Model):
    week = models.IntegerField(default=0)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)


class LabItem(models.Model):
    lab_time = models.IntegerField(default=0)
    is_available = models.BooleanField(default=False)
    change_available_tag = models.BooleanField(default=False)
    remaining_capacity = models.IntegerField(default=0)
    willing_user = models.ManyToManyField(User, related_name='willing')
    selected_user = models.ManyToManyField(User, related_name='selected')
    lab_week = models.ForeignKey(LabWeek, on_delete=models.CASCADE)

    def course_id(self):
        return self.lab_week.pk * 100 + self.lab_time

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

    def draw(self):
        max_capacity = self.lab_week.lab.lab_capacity
        self.remaining_capacity = max_capacity - self.selected_user.count()
        if self.willing_user.count() <= self.remaining_capacity:
            # all can select this lab
            for i in self.willing_user.all():
                self.selected_user.add(i)
        else:
            # randomize and add waiting list
            willing_range = self.willing_user.count()
            willing_user_list = self.willing_user.all()
            random_arr = [i for i in range(willing_range)]
            random.shuffle(random_arr)
            capacity = self.remaining_capacity
            for i in range(capacity):
                self.selected_user.add(willing_user_list[random_arr[i]])
            for i in range(capacity, len(random_arr)):
                wl_user = WaitingListUser()
                wl_user.lab_item = self
                wl_user.order_in_waiting_list = i - capacity + 1
                wl_user.user = willing_user_list[random_arr[i]]
                wl_user.save()
        self.willing_user.clear()
        self.remaining_capacity = max_capacity - self.selected_user.count()
        self.save()
        return

    class Meta:
        ordering = ['lab_time']


class WaitingListUser(models.Model):
    lab_item = models.ForeignKey(LabItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_in_waiting_list = models.IntegerField(default=0)

    class Meta:
        ordering = ['order_in_waiting_list']
