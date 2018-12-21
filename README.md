# Django-rest-api for site  "IT-school-on-the-React" 
https://github.com/Avderevo/IT-school-on-the-React

#### Need python 3.6+

## Install and Run:

#### 1 Customize the environment

#### 2 Download the repository:
```
$ git clone https://github.com/Avderevo/ITschool-djangorest-api

```

#### 3 Go to the directory with the file  ```manage.py```

#### 4 Install modules:

```
$ pip install requirements.txt
```

#### 5 Create migrations for the database:
``` 
$ python manage.py makemigrations users study
$ python manage.py migrate
```

#### !!! ( Для начала работы с курсами, нужно в ручную в админке добавить данные хотя бы для одного Курса - модели "Course" и пару уроков для этого курса - модель "Lesson" )

#### 6  Start project:

``` 
$ python manage.py runserver
```
