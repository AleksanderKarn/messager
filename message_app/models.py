from datetime import datetime
#import datetime
from django.db import models
from django.utils import timezone


##### посмотреть авторизацию


class Client(models.Model):  # переименовать клиент
    email = models.EmailField('Емейл адрес')
    full_name = models.CharField('Полное имя', max_length=250)
    comment = models.TextField('Комментарий')

    def __str__(self):
        return f'{self.full_name}, {self.email}, {self.comment}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    ONE_DAY = 'one_day'
    ONE_WEEK = 'one_week'
    ONE_MONTH = 'one_month'
    PERIODS = (
        ('one_day', 'раз в день'),
        ('one_week', 'раз в неделю'),
        ('one_month', 'раз в месяц')
    )
    STATUS_CREATE = 'create'
    STATUS_RUN = 'runner'
    STATUS_END = 'ended'
    STATUSES = (
        ('create', 'создана'),
        ('runner', 'запущена'),
        ('ended', 'завершена')
    )

    id_message = models.ForeignKey('Message', verbose_name='Выбрать письмо для рассылки', on_delete=models.SET_NULL,
                                   null=True)
    time_mailing_start = models.TimeField('Время начала рассылки', default=datetime.now(), null=True)
    time_mailing_end = models.TimeField('Время окончания рассылки', default=datetime.now(), null=True)
    period_mailing = models.CharField('Периодичность рассылки', choices=PERIODS, default=ONE_WEEK, max_length=50)
    status = models.CharField('Статус рассылки', choices=STATUSES, default=STATUS_CREATE, max_length=100)

    def __str__(self):
        return f'{self.time_mailing_start}, {self.period_mailing}, {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Message(models.Model):
    title = models.CharField('Тема письма', max_length=250)
    content = models.TextField('Содержание письма')



    def __str__(self):
        return f'{self.title}, {self.content}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class Attempt(models.Model):
    STATUS_RUN = 'runner'
    STATUS_END = 'ended'
    STATUSES_ATTEMPT = (
        'runner', 'исполняется',
        'ended', 'закончена'
    )
    date_time = models.DateTimeField('Дата и время последней попытки', default=datetime.now())
    status_attempt = models.CharField('Статус попытки', default=STATUS_RUN, max_length=10)
    answer = models.CharField('Ответ почтового сервера', max_length=250, default=200)
    mailing_id = models.IntegerField('Id рассылки', null=True)


    def __str__(self):
        return f'{self.date_time}, {self.status_attempt}, {self.answer}'

    class Meta:
        verbose_name = 'Попытка '
        verbose_name_plural = 'Попытки'


class MailingToClient(models.Model):
    mailing = models.IntegerField('ID рассылки')
    client = models.IntegerField('ID Клиента')
