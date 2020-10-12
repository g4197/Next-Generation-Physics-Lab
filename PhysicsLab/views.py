from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import models
from django.db.models import Max
from .models import WeekStatus, Lab, LabWeek, LabItem, WaitingListUser
import datetime


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('PhysicsLab:query', args=[get_current_week()]))
    else:
        return HttpResponseRedirect(reverse('PhysicsLab:lab_login'))


def render_error(request, error_message: str):
    return render(request, 'error.html', {
        'window_title': '错误',
        'alert_placeholder': error_message,
    })


def student_register(request):
    return render(request, 'register.html', {
        'window_title': '注册',
    })


def student_register_handler(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        student_id = int(username)
    except KeyError or ValueError:
        return render_error(request, '学号或密码输入有误')

    # check if exists
    database_user = User.objects.filter(username=username)
    if database_user:
        return render_error(request, '用户已存在')

    # id limit
    if not 2019000001 <= student_id <= 2019099999:
        return render_error(request, '学号错误')

    # password length limit
    if not 6 <= len(password) <= 16:
        return render_error(request, '密码长度不符合要求')

    user = User.objects.create_user(username=username, password=password)
    user.save()
    return HttpResponseRedirect(reverse('PhysicsLab:index'))


def lab_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('PhysicsLab:query'))
    return render(request, 'login.html', {
        'window_title': '登录',
    })


def lab_login_handler(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return HttpResponseRedirect(reverse('PhysicsLab:query', args=[get_current_week()]))
    else:
        return render_error(request, '用户名或密码错误')


def lab_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('PhysicsLab:lab_login'))


def admin_add_lab(request):
    if request.user.has_perm('PhysicsLab:admin_add_lab'):
        return render(request, 'admin_add_lab.html', {
            'window_title': '添加实验',
        })
    return HttpResponseRedirect(reverse('PhysicsLab:index'))


def admin_add_lab_handler(request):
    if not request.user.has_perm('PhysicsLab.add_lab'):
        return HttpResponseRedirect(reverse('PhysicsLab:index'))
    try:
        lab_name = request.POST.get('lab_name', '')
        lab_capacity = int(request.POST.get('lab_capacity', '0'))
        lab_place = request.POST.get('lab_place', '')
    except ValueError:
        return HttpResponseRedirect(reverse('PhysicsLab:admin_add_lab'))
    if lab_name and lab_capacity and lab_place:
        lab = Lab()
        lab.lab_capacity = lab_capacity
        lab.lab_place = lab_place
        lab.lab_name = lab_name
        lab.save()
        for week in range(1, 17):
            lab_week = LabWeek()
            lab_week.week = week
            lab_week.lab = lab
            lab_week.save()
            for i in range(21):
                lab_item = LabItem()
                lab_item.lab_week = lab_week
                lab_item.is_available = False
                lab_item.lab_time = (i // 3 + 1) * 10 + i % 3 + 1
                lab_item.save()
        return HttpResponseRedirect(reverse('PhysicsLab:admin_add_lab'))


def admin_modify_lab(request):
    if not request.user.has_perm('PhysicsLab:change_lab'):
        return HttpResponseRedirect(reverse('PhysicsLab:index'))
    try:
        week = int(request.GET.get('week', 0))
    except ValueError:
        week = 0
    lab_list = LabWeek.objects.filter(week=week).order_by('pk')
    return render(request, 'admin_modify_lab.html', {
        'window_title': '修改第' + str(week) + '周实验',
        'week_list': ['一', '二', '三', '四', '五', '六', '日'],
        'lab_list': lab_list,
        'cur_modify_week': week,
    })


def admin_modify_lab_handler(request):
    if not request.user.has_perm('PhysicsLab:change_lab'):
        return HttpResponseRedirect(reverse('PhysicsLab:index'))
    try:
        week = int(request.POST.get('week', 0))
    except ValueError:
        return HttpResponseRedirect(reverse('PhysicsLab:admin_modify_lab'))
    modify_list = map(int, request.POST.getlist('course_id'))
    if week:
        cur_week_lab_item = LabItem.objects.filter(lab_week__week=int(week))
        for i in cur_week_lab_item:
            i.is_available = False
            i.selected_user.clear()
            i.willing_user.clear()
            i.waitinglistuser_set.all().delete()
            i.remaining_capacity = 0
            i.save()
        for i in modify_list:
            modify_lab = cur_week_lab_item.get(lab_week__pk=i / 100, lab_time=i % 100)
            modify_lab.is_available = True
            if is_drawn():
                modify_lab.remaining_capacity = modify_lab.lab_week.lab.lab_capacity - modify_lab.selected_user.count()
            else:
                modify_lab.remaining_capacity = modify_lab.lab_week.lab.lab_capacity
            modify_lab.save()
    return HttpResponseRedirect(reverse('PhysicsLab:admin_modify_lab') + '?week=' + str(week))


def admin_remove_lab(request):
    if not request.user.has_perm('PhysicsLab:remove_lab'):
        return HttpResponseRedirect(reverse('PhysicsLab:index'))
    lab_name = request.GET.get('name', '')
    lab_list = []
    if lab_name:
        # for lab can repeat several times with different weeks, I will only use week 1 for query.
        lab_list = Lab.objects.filter(lab_name__icontains=lab_name)
    return render(request, 'admin_remove_lab.html', {
        'window_title': '删除实验',
        'lab_list': lab_list,
    })


def admin_remove_lab_handler(request):
    if not request.user.has_perm('PhysicsLab:remove_lab'):
        return HttpResponseRedirect(reverse('PhysicsLab:index'))
    lab_pk = request.POST.get('lab_pk', -1)
    if lab_pk != -1:
        lab = Lab.objects.get(pk=lab_pk)
        lab.delete()
    return HttpResponseRedirect(reverse('PhysicsLab:admin_remove_lab'))


def query_lab(request, week: int):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('PhysicsLab:lab_login'))
    lab_list = LabWeek.objects.filter(week=week).order_by('pk')
    selected_lab = 0
    for i in request.user.willing.all():
        selected_lab = i.course_id()
    for i in request.user.selected.all():
        selected_lab = i.course_id()
    for i in request.user.waitinglistuser_set.all():
        selected_lab = i.lab_item.course_id()
    all_selected_lab = request.user.selected.all().order_by('lab_time')
    all_willing_lab = request.user.willing.all().order_by('lab_time')
    all_wl_lab = request.user.waitinglistuser_set.all().order_by('lab_item__lab_time')
    return render(request, 'query_lab.html', {
        'window_title': '查询第' + str(week) + '周实验',
        'week_list': ['一', '二', '三', '四', '五', '六', '日'],
        'lab_list': lab_list,
        'selected_lab': selected_lab,
        'is_drawn': is_drawn(),
        'all_selected_lab': all_selected_lab,
        'all_willing_lab': all_willing_lab,
        'all_wl_lab': all_wl_lab,
    })


def select_lab_handler(request):
    if not request.user.is_authenticated:
        return render_error(request, '您还未登录')
    try:
        course_id = int(request.POST.get('course_id', -1))
    except ValueError:
        return HttpResponseRedirect(reverse('PhysicsLab:query'))
    if course_id == -1:
        return HttpResponseRedirect(reverse('PhysicsLab:query'))

    # first check if previous course equal to current course
    cur_course_id = 0
    for w_user in request.user.waitinglistuser_set.all():
        cur_course_id = w_user.lab_item.course_id()
    for lab in request.user.selected.all():
        cur_course_id = lab.course_id()
    for lab in request.user.willing.all():
        cur_course_id = lab.course_id()
    if cur_course_id == course_id:
        return HttpResponseRedirect(reverse('PhysicsLab:query', args=[get_current_week()]))

    cur_week = get_current_week()
    lab_id = course_id / 100
    lab_time = course_id % 100
    try:
        lab = LabItem.objects.get(lab_week__pk=lab_id, lab_time=lab_time)
    except models.ObjectDoesNotExist:
        lab = None
    if is_drawn():
        # remove waiting list course this week, it removes the user itself.
        for self_w_user in request.user.waitinglistuser_set.filter(lab_item__lab_week__week=cur_week):
            cur_user_order = self_w_user.order_in_waiting_list
            for w_user in self_w_user.lab_item.waitinglistuser_set.all():
                if w_user.order_in_waiting_list > cur_user_order:
                    w_user.order_in_waiting_list -= 1
                    w_user.save()
            self_w_user.delete()

        # remove last course this week
        for lab_item in request.user.selected.filter(lab_week__week=cur_week):
            wl_set = lab_item.waitinglistuser_set.all()
            if not wl_set:
                lab_item.remaining_capacity += 1

            # have waiting list user, give the course to the queue top
            for w_user in wl_set:
                w_user.order_in_waiting_list -= 1
                w_user.save()
                if w_user.order_in_waiting_list == 0:
                    lab_item.selected_user.add(w_user.user)
                    w_user.delete()
            lab_item.selected_user.remove(request.user)
            lab_item.save()

        # select current course
        if lab:
            if lab.remaining_capacity > 0:
                lab.remaining_capacity -= 1
                request.user.selected.add(lab)
            else:
                # add to waiting list
                wl_user = WaitingListUser()
                wl_user.user = request.user

                # wl is consistent, so just use count.
                max_wl_order = lab.waitinglistuser_set.count()
                wl_user.order_in_waiting_list = max_wl_order + 1
                wl_user.lab_item = lab
                wl_user.save()
            lab.save()
        return HttpResponseRedirect(reverse('PhysicsLab:query', args=[cur_week]))

    # lab is available
    for i in request.user.willing.filter(lab_week__week=cur_week):
        request.user.willing.remove(i)
    request.user.willing.add(lab)
    request.user.save()
    if course_id != 0:
        lab.willing_user.add(request.user)
        lab.save()
    return HttpResponseRedirect(reverse('PhysicsLab:query', args=[cur_week]))


def get_current_week():
    return (datetime.datetime.now().date() - datetime.date(2020, 9, 14)).days // 7 + 1


def draw():
    pass

def is_drawn():
    drawn = WeekStatus.objects.get(week=get_current_week()).is_drawn
    return drawn
