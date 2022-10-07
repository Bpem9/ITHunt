from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .models import *
from .filters import *
from .GdrvtoSQL.stuff import lst_juns, hrds, tolls, sfts, poss, countries
from slugify import slugify
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm
from .forms import *




class JuniorPage(DetailView):
    model = Junior
    template_name = 'juniors/jun.html'
    context_object_name = 'junior'
    slug_url_kwarg = 'jun_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Страница джуна'
        context['jun_slug'] = self.kwargs['jun_slug']
        context['softskills_full'] = SoftSkills.objects.all()
        context['hardskills_full'] = Hardskills.objects.all()
        context['tools_full'] = Tools.objects.all()
        return context
    def get_queryset(self):
        sfkl = self.request.GET.getlist('softskills')
        hdkl = self.request.GET.getlist('hardskills')
        tlls = self.request.GET.getlist('tools')
        return Junior.objects.filter(slug=self.kwargs['jun_slug'])

class JuniorsView(ListView):
    model = Junior
    template_name = 'juniors/index.html'
    context_object_name = 'juniors'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pos_selected'] = 0
        context['softskills_a'] = SoftSkills.objects.filter(jun__in=context['object_list']).distinct()
        context['tools_a'] = Tools.objects.filter(jun__in=context['object_list']).distinct()
        context['hardskills_a'] = Hardskills.objects.filter(jun__in=context['object_list']).distinct()
        context['search'] = SearchFilter(self.request.GET, queryset=Junior.objects.all())
        return context

    def get_queryset(self):
        # <------------------- БДшка------------------->
        # for i in range(len(lst_juns)):
        #     Junior(id=i, first_name=lst_juns[i].first_name, last_name=lst_juns[i].last_name, slug=lst_juns[i].slug, linkedin=lst_juns[i].linkedin,
        #            telegram=lst_juns[i].telegram, email=lst_juns[i].email, descr=lst_juns[i].descr, language=lst_juns[i].lang, exp=lst_juns[i].exp).save()
        # for tool in tolls:
        #     Tools(tool=tool).save()
        # for hdskill in hrds:
        #     Hardskills(skill=hdskill).save()
        # for sfskill in sfts:
        #     SoftSkills(skill=sfskill).save()
        # for pos in poss:
        #     Position(position=pos, slug=slugify(pos)).save()
        # for coun in countries:
        #     Country(country=coun, slug=slugify(coun)).save()
        # Заполнение БД из файла GdrvtoSQL (из таблицы google-drive), запускать один раз, в случае, если нужно пересоздать БД базового состояния
        # <------------------- БДшка------------------->
        search = SearchFilter(self.request.GET, queryset=Junior.objects.all())
        sfkl = self.request.GET.getlist('softskills')
        hdkl = self.request.GET.getlist('hardskills')
        tlls = self.request.GET.getlist('tools')
        if search.qs:
            juniors = search.qs
        if sfkl:
            juniors = juniors.filter(softskills__skill__in=sfkl)
        if hdkl:
            juniors = juniors.filter(hardskills__skill__in=hdkl)
        if tlls:
            juniors = juniors.filter(tools__tool__in=tlls)
        return juniors
        # ''' Стартовая выборка - все джуны из БД.
        #      Если метод GET что-то возвращает - все значения записываются в виде списка скиллов в skfl, hkdl или tlls.
        #      В новую выборку джунов отфильтовываются джуны из стартовой выборки БД в атрибуте softskills/hardskills/tools__skill
        #      (из вторичной модели softskills, hardskills или tools) которых содержатся скиллы из skfl, hdkl ли tlls.
        #      Список джунов подается в шаблон html. '''

class JuniorsPosition(ListView):
    model = Junior
    template_name = 'juniors/index.html'
    context_object_name = 'juniors'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Страница категории'
        context['softskills_a'] = SoftSkills.objects.filter(jun__in=context['object_list']).distinct()
        context['tools_a'] = Tools.objects.filter(jun__in=context['object_list']).distinct()
        context['hardskills_a'] = Hardskills.objects.filter(jun__in=context['object_list']).distinct()
        context['pos_selected'] = self.kwargs['pos_id']
        context['search'] = SearchFilter(self.request.GET, queryset=Junior.objects.all())
        return context

    def get_queryset(self):
        juniors = Junior.objects.filter(position_id=self.kwargs['pos_id'])
        search = SearchFilter(self.request.GET, queryset=juniors)
        if search.qs:
            juniors = search.qs
        sfkl = self.request.GET.getlist('softskills')
        hdkl = self.request.GET.getlist('hardskills')
        tlls = self.request.GET.getlist('tools')
        if sfkl:
            juniors = juniors.filter(softskills__skill__in=sfkl)
        if hdkl:
            juniors = juniors.filter(hardskills__skill__in=hdkl)
        if tlls:
            juniors = juniors.filter(tools__tool__in=tlls)
        return juniors


class JuniorProfile(DetailView):
    model = User
    template_name = 'juniors/profile.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        return context

    def get_object(self, queryset=None):
        return self.request.user


class RegisterJunior(CreateView):
    form_class = UserRegForm
    template_name = 'juniors/registration.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Страница регистрации'
        return context

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'juniors/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context
    def get_success_url(self):
        return reverse_lazy('index')

def userlogout(request):
    logout(request)
    return redirect('index')