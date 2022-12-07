import gspread
from slugify import slugify



gc = gspread.service_account()
URL = 'https://docs.google.com/spreadsheets/d/1QfmafovfVCDsxbUIqXi8BOz41nayuqT5JMdUoP9uPlE/edit#gid=0'

class Junior:
    def __init__(self, first_name, last_name, position, linkedin, email, telegram, location, descr, tools, soft, hard, lang, exp):
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.position = position.strip()
        self.slug = slugify(self.last_name)
        self.linkedin = linkedin
        self.email = email.strip()
        self.telegram = telegram.replace('@', 'https://t.me/')
        self.location = location.strip()
        self.descr = descr.strip()
        self.tools = tools
        self.soft = soft
        self.hard = hard
        self.lang = lang
        self.exp = exp
    # def __repr__(self):
    #     return self.first_name + ' ' + self.last_name
    def __repr__(self):
        return f'first_name=\'{self.first_name}\', ' \
               f'last_name=\'{self.last_name}\', ' \
               f'linkedin=\'{self.linkedin}\', ' \
               f'telegram=\'{self.telegram}\', ' \
               f'email=\'{self.email}\', ' \
               f'role=\'{self.position}\', ' \
               f'exp=\'{self.exp}\' '
               # f'descr=\'{self.descr}\''

    def show(self):
        return f'[Имя: {self.first_name}\n ' \
               f'Фамилия: {self.last_name}\n ' \
               f'Должность: {self.position}\n ' \
               f'Профиль на Linkedin: {self.linkedin}\n ' \
               f'Электронная почта: {self.email}]\n ' \
               f'Профиль в телеграм :{self.telegram}\n ' \
               f'Место проживания: {self.location}\n ' \
               f'Описание: {self.descr}\n ' \
               f'Стек технологий: {self.tools}\n ' \
               f'Софт-скиллы: {self.soft}\n ' \
               f'Хард-скиллы: {self.hard}\n ' \
               f'Язык: {self.lang}\n ' \
               f'Опыт работы: {self.exp}]'

table = gc.open_by_url(URL)
wsh = table.worksheet('Лист1')
titles = wsh.row_values(1)
names = wsh.col_values(1)[:13]
lst_juns = []
for i in range(2, len(names)+1):
    lst_juns.append(Junior(*wsh.row_values(i)[:13]))
# print(lst_juns[2].telegram)

tolls = []
for i in lst_juns:
    [tolls.append(tool) for tool in i.tools.split(', ')]
tolls = list(set(tolls))
# print(f'Tools: ', tolls)
print('='*50)
hrds = []
for i in lst_juns:
    [hrds.append(hrd.capitalize()) for hrd in i.hard.split(', ')]
hrds = list(set(hrds))
# print(f'Hardskills: ', hrds)
print('='*50)
sfts = []
for i in lst_juns:
    [sfts.append(sft.capitalize()) for sft in i.soft.split(', ')]
sfts = list(set(sfts))
poss = []
for i in lst_juns:
    [poss.append(pos) for pos in i.position.split(', ')]
poss = list(set(poss))

messengers = ['LinkedIn', 'Telegram', 'What\'s up', 'Viber', 'Facebook', 'Вконтакте', 'Email',
              'Instagram', 'Behance', 'Pinterest', 'Website']

countries = ['Беларусь', 'Республика Кипр', 'Германия', 'Украина', 'Болгария', 'Грузия']

# print(f'Softskills: ', sfts)
# tools = list(set(tools))
# print(tools)

# for i in lst_juns:
#      Junior(id=i, first_name=i.first_name, last_name=i.last_name, role=i.position,  slug=i.slug, linkedin=i.linkedin, telegram=i.telegram, email=i.email, descr=i.descr, language=i.lang, exp=i.exp).save()
