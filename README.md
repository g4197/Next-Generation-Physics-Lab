# Fake-Physics-Lab

### 简介

* 这是一个假冒物理实验选课系统
* 仿照`166.111.214.78`制作
* 还没做完

### 构建方法

* 需求：`python`与`django`

* 在源码目录运行

* ````shell
  python(3) manage.py makemigrations
  python(3) manage.py migrate
  python(3) manage.py shell < init_global.py
  python(3) manage.py runserver
  ````

* 服务器将会启动在`localhost:8000`