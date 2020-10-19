# Next Generation PhysicsLab

### 简介

* 这可能是下一代物理实验选课系统的demo版
* 仿照`166.111.214.78`制作

### 构建方法

* 需求：`python`与`django`

* 在源码目录运行（`Windows`环境）

* ````shell
  python manage.py makemigrations
  python manage.py migrate
  python manage.py shell < init_global.py
  python manage.py runserver
  ````

* 如果是`linux`环境下，则把上述命令中`python`更改为`python3`

* 服务器将会启动在`localhost:8000`

### 超级用户创建

* 本系统的用户完全与`django.auth`对接，创建用户命令与`django`相同，即`python manage.py createsuperuser username`，然后按照提示操作

### 未完成功能

* 加入实验讲义等资源
* 每周每个用户可选多个实验
* 自动抽签（利用`cron`任务即可实现）

