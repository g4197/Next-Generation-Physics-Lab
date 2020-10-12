from django.urls import path
from . import views

app_name = 'PhysicsLab'
urlpatterns = [
    path('', views.index, name='index'),
    path('query/<int:week>/', views.query_lab, name='query'),
    path('register/', views.student_register, name='student_register'),
    path('submit_register', views.student_register_handler, name='submit_student_register'),
    path('login/', views.lab_login, name='lab_login'),
    path('submit_login/', views.lab_login_handler, name='submit_lab_login'),
    path('logout/', views.lab_logout, name='lab_logout'),
    path('select/', views.select_lab_handler, name='select'),
    path('lab_admin/add/', views.admin_add_lab, name='admin_add_lab'),
    path('lab_admin/submit_add/', views.admin_add_lab_handler, name='submit_admin_add'),
    path('lab_admin/modify/', views.admin_modify_lab, name='admin_modify_lab'),
    path('lab_admin/submit_modify/', views.admin_modify_lab_handler, name='submit_admin_modify'),
    path('lab_admin/submit_draw/', views.admin_draw_handler, name='submit_admin_draw'),
    path('lab_admin/remove/', views.admin_remove_lab, name='admin_remove_lab'),
    path('lab_admin/submit_remove/', views.admin_remove_lab_handler, name='submit_admin_remove'),
]
