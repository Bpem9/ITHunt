from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.models import User


class Junior(models.Model):
    username = models.OneToOneField(User, null=True, verbose_name='Пользователь', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Фамилия')
    slug = models.SlugField(max_length=100, unique=True, blank=True, db_index=True, verbose_name='URL')
    linkedin = models.CharField(max_length=100, null=True, blank=True, verbose_name='Профиль Linkedin')
    telegram = models.CharField(max_length=100, null=True, blank=True, verbose_name='Профиль Telegram')
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name='Электронная почта')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Номер телефона')
    url_img = models.ImageField(upload_to="photos/%Y/%m/%d", blank=True, null=True, verbose_name='Фото')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    position = models.ForeignKey('Position', null=True, blank=True, default=6, on_delete=models.PROTECT)
    country = models.ForeignKey('Country', null=True, blank=True, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    exp = models.CharField(null=True, max_length=20)
    language = models.CharField(max_length=100, null=True, blank=True, verbose_name='Языки')
    salary = models.IntegerField(null=True, blank=True)


    class Meta:
        verbose_name = 'Джуны'
        verbose_name_plural = 'Джуны'
        ordering = ['id']

    def __str__(self):
        return str(self.username)

    def get_absolute_url(self):
        return reverse('junior', kwargs={'jun_slug': self.slug, 'pos_slug': self.position.slug})


class Country(models.Model):
    country = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='Страна')
    image = models.FileField(upload_to="country", blank=True, verbose_name='Иконка-флаг')

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'
        ordering = ['id']

    def __str__(self):
        return self.country

    def get_absolute_url(self):
        return reverse('country', kwargs={'country_id': self.pk})


class Position(models.Model):
    position = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, default='backend', db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Специальности'
        verbose_name_plural = 'Специальности'
        ordering = ['id']

    def __str__(self):
        return str(self.position)

    def get_absolute_url(self):
        return reverse('position', kwargs={'pos_slug': self.slug})


# ===========================

class SoftSkills(models.Model):
    skill = models.CharField(max_length=100)
    jun = models.ManyToManyField(Junior, through='JuniorSoftskills')

    class Meta:
        verbose_name = 'Софт-скилл'
        verbose_name_plural = 'Софт-скиллы'
        ordering = ['id']

    def __str__(self):
        return self.skill

    def get_absolute_url(self):
        return reverse('softskills', kwargs={'sf_id': self.pk})


class JuniorSoftskills(models.Model):
    skill = models.ForeignKey('SoftSkills', on_delete=models.PROTECT)
    junior = models.ForeignKey('Junior', on_delete=models.PROTECT)

    class Meta:
        unique_together = [['junior', 'skill']]
        verbose_name = 'Связь Джун - Софт-скилл'
        verbose_name_plural = 'Связи Джун - Софт-скилл'

    def __str__(self):
        return f'{self.junior} - {self.skill}'


# ===========================

class Tools(models.Model):
    tool = models.CharField(max_length=100)
    jun = models.ManyToManyField(Junior, through='JuniorTools')

    class Meta:
        verbose_name = 'Технология'
        verbose_name_plural = 'Стек технологий'

    def __str__(self):
        return self.tool

    def get_absolute_url(self):
        return reverse('tools', kwargs={'tl_id': self.pk})


class JuniorTools(models.Model):
    skill = models.ForeignKey('Tools', on_delete=models.PROTECT)
    junior = models.ForeignKey('Junior', on_delete=models.PROTECT)

    class Meta:
        unique_together = [['junior', 'skill']]
        verbose_name = 'Связь Джун - Технология'
        verbose_name_plural = 'Связи Джун - Технология'

    def __str__(self):
        return f'{self.junior} - {self.skill}'


# ===========================

class Hardskills(models.Model):
    skill = models.CharField(max_length=100)
    jun = models.ManyToManyField(Junior, through='JuniorHardskills')

    class Meta:
        verbose_name = 'Хард-скилл'
        verbose_name_plural = 'Хард-скиллы'

    def __str__(self):
        return self.skill

    def get_absolute_url(self):
        return reverse('hardskills', kwargs={'hd_id': self.pk})


class JuniorHardskills(models.Model):
    skill = models.ForeignKey('Hardskills', on_delete=models.PROTECT)
    junior = models.ForeignKey('Junior', on_delete=models.PROTECT)

    class Meta:
        unique_together = [['junior', 'skill']]
        verbose_name = 'Связь Джун - Хард-скилл'
        verbose_name_plural = 'Связи Джун - Хард-скилл'

    def __str__(self):
        return f'{self.junior} - {self.skill}'


# ===========================

class JunSchedule(models.Model):
    junior_id = models.ForeignKey('Junior', on_delete=models.CASCADE, related_name='junior')
    client_id = models.ForeignKey('Junior', on_delete=models.CASCADE, null=True, related_name='client')
    date = models.DateField(blank=True)
    time = models.TimeField(blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(time__in=('13:00', '14:00', '15:00')), name='valid_hours_constraint'),
            models.UniqueConstraint(fields=('junior_id', 'client_id', 'date', 'time'),
                                    name='single_appointment_constraint'),

        ]

    def __str__(self):
        return f'{self.client_id} appointed to {self.junior_id} in {self.date}, {self.time}'

class Messengers(models.Model):
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name='Эл. почта для связи')
    website = models.CharField(max_length=100, null=True, blank=True, verbose_name='Вебсайт')
    whatsup = models.CharField(max_length=100, null=True, blank=True, verbose_name='Профиль Whatsapp')
    viber = models.CharField(max_length=100, null=True, blank=True, verbose_name='Профиль Viber')
    facebook = models.CharField(max_length=100, null=True, blank=True, verbose_name='Профиль Facebook')
    vk = models.CharField(max_length=100, null=True, blank=True, verbose_name='Профиль Вконтакте')
    instagram = models.CharField(max_length=100, null=True, blank=True, verbose_name='Профиль Instagram')
    behance = models.CharField(max_length=100, null=True, blank=True, verbose_name='Профиль Behance')
    pinterest = models.CharField(max_length=100, null=True, blank=True, verbose_name='Профиль Piterest')
    junior = models.ForeignKey(Junior, on_delete=models.CASCADE, null=True, blank=True, related_name='owner')

    class Meta:
        verbose_name = 'Мессенджер'
        verbose_name_plural = 'Мессенджеры'

    def __str__(self):
        return f'Мессенджеры {self.junior}'

