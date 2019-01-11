# ITschool-djangorest-api 

##  This is the api for React spa application: https://github.com/Avderevo/IT-school-on-the-React 




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

#### 6 Loading initial data:

```
$ python manage.py loaddata course.json lessons.json

```
#### 7  Run the configuration:

```
$ export DJANGO_CONFIGURATION=Dev
```
#### 8 Run Server Dev:

``` 
$ python manage.py runserver
```
## Run test 
```
$ python manage.py test


```
