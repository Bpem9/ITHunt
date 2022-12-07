from slugify import slugify
from .GdrvtoSQL.stuff import lst_juns, hrds, tolls, sfts, poss, countries, messengers
from .models import *


class DBFiller:
    """
        Заполнение БД из файла GdrvtoSQL (из таблицы google-drive), запускать один раз, в случае,
        если нужно пересоздать БД базового состояния
    """
    @staticmethod
    def juniors_filling():
        """Заполнение таблицы джунов"""
        for i in range(len(lst_juns)):
            Junior(id=i, first_name=lst_juns[i].first_name, last_name=lst_juns[i].last_name, slug=lst_juns[i].slug, linkedin=lst_juns[i].linkedin,
                   telegram=lst_juns[i].telegram, email=lst_juns[i].email, descr=lst_juns[i].descr, language=lst_juns[i].lang, exp=lst_juns[i].exp).save()

    @staticmethod
    def tools_filling():
        """Заполнение таблицы джунов"""
        for tool in tolls:
            Tools(tool=tool).save()

    @staticmethod
    def hardskills_filling():
        """Заполнение таблицы хардскиллов"""
        for hdskill in hrds:
            Hardskills(skill=hdskill).save()

    @staticmethod
    def softskills_filling():
        """Заполнение таблицы софтскиллов"""
        for sfskill in sfts:
            SoftSkills(skill=sfskill).save()

    @staticmethod
    def positions_filling():
        """Заполнение таблицы позиций"""
        for pos in poss:
            Position(position=pos, slug=slugify(pos)).save()

    @staticmethod
    def countries_filling():
        """Заполнение таблицы локаций"""
        for coun in countries:
            Country(country=coun, slug=slugify(coun)).save()

    @staticmethod
    def messengers_filling():
        """Заполнение таблицы мессенджеров"""
        for mess in messengers:
            Messengers.objects.update_or_create(name=mess)

    def full_filling(self):
        self.juniors_filling()
        self.tools_filling()
        self.hardskills_filling()
        self.softskills_filling()
        self.positions_filling()
        self.countries_filling()
        self.messengers_filling()
