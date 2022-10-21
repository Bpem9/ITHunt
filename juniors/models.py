from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# class Junior(models.Model):
#     fio = models.CharField(max_length=250, null=True, verbose_name='ФИО Специалиста')
#     slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name='URL')
#     exp = models.CharField(max_length=250)
#     salary = models.IntegerField()
#     cat = models.ForeignKey('Category', on_delete=models.PROTECT)
#
#     class Meta:
#         verbose_name = 'Джуны'
#         verbose_name_plural = 'Джуны'
#         ordering=['id']
#
#     def __str__(self):
#         return self.fio
#
#     def get_absolute_url(self):
#         return reverse('junior', kwargs={'jun_slug': self.slug, 'cat_id': self.cat})
# =======Junior================
class Junior(models.Model):
    username = models.OneToOneField(User, null=True, verbose_name='Пользователь', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=50, null=True, verbose_name='Фамилия')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')
    linkedin = models.CharField(max_length=100, null=True, verbose_name='Профиль Linkedin')
    telegram = models.CharField(max_length=100, null=True, verbose_name='Профиль Telegram')
    email = models.CharField(max_length=100, null=True, verbose_name='Электронная почта')
    phone = models.CharField(max_length=20, null=True, verbose_name='Номер телефона')
    url_img = models.ImageField(upload_to="photos/%Y/%m/%d", null=True, verbose_name='Фото')
    description = models.TextField(null=True, verbose_name='Описание')
    position = models.ForeignKey('Position', null=True, on_delete=models.PROTECT)
    country = models.ForeignKey('Country', null=True, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    exp = models.CharField(null=True, max_length=20)
    language = models.CharField(max_length=100, null=True, verbose_name='Языки')
    salary = models.IntegerField(null=True)
    password=models.CharField(max_length=50, null=True, verbose_name='Пароль')
    # sfskills = models.ManyToManyField('SoftSkills', null=True, verbose_name='Софт-скиллы')
    # hdskills = models.ForeignKey('Hardskills', null=True, on_delete=models.PROTECT, verbose_name='Хард-скиллы')
    # tlls = models.ForeignKey('Tools', null=True, on_delete=models.PROTECT, verbose_name='Стек технологий')

    class Meta:
        verbose_name = 'Джуны'
        verbose_name_plural = 'Джуны'
        ordering=['id']

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('junior', kwargs={'jun_slug': self.slug, 'pos_slug': self.position.slug})

class Country(models.Model):
    country = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='Страна')
    image = models.FileField(upload_to="country", blank=True, verbose_name='Иконка-флаг')

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'
        ordering=['id']

    def __str__(self):
        return self.country

    def get_absolute_url(self):
        return reverse('country', kwargs={'country_id': self.pk})


class Position(models.Model):
    position = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')
    # flag = models.

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

