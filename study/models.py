from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name_1 = models.CharField(max_length=50, verbose_name='Курс')
    name_2 = models.CharField(max_length=50)
    homework_all = models.IntegerField(blank=True, verbose_name='Всего домашек')
    description = models.TextField(blank=True)
#    date_start = models.CharField(max_length=50, blank=True)
#    label = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Курсы'
        verbose_name = 'Курс'

    def __str__(self):
        return f'Курс {self.name_1}'


class CourseStatistic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    homework_done = models.IntegerField(default=0, verbose_name='Сделанных домашек')
    is_active = models.BooleanField(default=False, verbose_name='Сдал тест')
    is_paid = models.BooleanField(default=False, verbose_name='Курс оплачен')

    def __str__(self):
        return f'Статистика курса {self.user} {self.course}'

    class Meta:
        verbose_name = "Статистика курса"
        verbose_name_plural = 'Статистика курсов'


class Lesson(models.Model):
    lesson_title = models.CharField(max_length=125, verbose_name='Название урока')
    is_homework = models.BooleanField(default=False)
    homework_title = models.CharField(max_length=125, blank=True, verbose_name='Домашнее задание' )
    lesson_number = models.IntegerField(verbose_name='Номер урока')
#    date_start = models.DateTimeField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')

    def __str__(self):
        return f'{self.lesson_title} Урок N {self.lesson_number} - {self.homework_title}'

    class Meta:
        verbose_name="Урок"
        verbose_name_plural = 'Уроки'


class LessonStatistic(models.Model):
    HOMEWORK_STATUS = (
        (1 , 'not active'),
        (2, 'active'),
        (3, 'on check '),
        (4, 'done')
    )
    homework_status = models.CharField(max_length=15, choices=HOMEWORK_STATUS, default=1, verbose_name='Статус домашнего задания')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Студент')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')

    class Meta:
        verbose_name = 'Статистика урока'
        verbose_name_plural = 'Статистика уроков'

    def __str__(self):
        return f"Статистика {self.user} урок {self.lesson}"




class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_body = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    lesson_statistic = models.ForeignKey(LessonStatistic, on_delete=models.CASCADE)


    def __str__(self):
        return 'Сообщение'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'










