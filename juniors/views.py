from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin, ModelFormMixin

from .models import *
from .filters import *
from .GdrvtoSQL.stuff import lst_juns, hrds, tolls, sfts, poss, countries
from slugify import slugify
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import *
from .utils import SkillsFilters, SkillControl
from django.db.models import Max




class JuniorPage(DetailView):
    model = Junior
    template_name = 'juniors/jun.html'
    context_object_name = 'junior'
    slug_url_kwarg = 'jun_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Страница джуна'
        context['search'] = SearchFilter(self.request.GET, queryset=Junior.objects.all())
        return context


class JuniorsView(SkillsFilters, ListView):
    model = Junior
    template_name = 'juniors/index.html'
    context_object_name = 'juniors'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Джуны'
        context['order'] = ['По алфавиту', 'По рейтингу', 'По зарплате', 'По локации']
        context['search'] = SearchFilter(self.request.GET, queryset=context['object_list'])
        return context


    def get_queryset(self, **kwargs):
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
        juniors = super().get_filtrated_queryset(**self.kwargs)
        return super().get_sorted_queryset(juniors)


class JuniorsPosition(SkillsFilters, ListView):
    model = Junior
    template_name = 'juniors/index.html'
    context_object_name = 'juniors'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Страница категории'
        context['order'] = ['По алфавиту', 'По рейтингу', 'По зарплате', 'По локации']
        context['search'] = SearchFilter(self.request.GET, queryset=context['object_list'])
        return context

    def get_queryset(self):
        juniors = super().get_filtrated_queryset(**self.kwargs)
        return super().get_sorted_queryset(juniors)


class JuniorProfile(SkillControl, DetailView):
    model = Junior
    template_name = 'juniors/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        context['search'] = SearchFilter(self.request.GET, queryset=Junior.objects.all())
        context['hardskills'] = Hardskills.objects.all()
        context['softskills'] = SoftSkills.objects.all()
        context['tools'] = Tools.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        ac = request.GET.get('ac')
        if ac == 'add':
            self._add_skill(request, *args, **kwargs)
        elif ac == 'del':
            self._del_skill(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    # def get_initial(self):
    #     initial = super().get_initial()
    #     jun = self.request.user.junior
    #     initial['first_name'] = jun.first_name
    #     initial['last_name'] = jun.last_name
    #     initial['position'] = jun.position
    #     initial['description'] = jun.description
    #     return initial

    def _add_skill(self, request, *args, **kwargs):
        try:
            super()._add_skill(self, request, *args, **kwargs)
        except Exception as e:
            print(e)
        return super().get(request, *args, **kwargs)

    def _del_skill(self, request, *args, **kwargs):
        try:
            super()._del_skill(self, request, *args, **kwargs)
        except Exception as e:
            print(e)
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return Junior.objects.get(slug=self.kwargs['jun_slug'])


class JuniorUpdate(UpdateView):
    model = Junior
    form_class = JunUpdatingForm
    template_name = 'juniors/profile_update.html'
    slug_url_kwarg = 'jun_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = SearchFilter(self.request.GET, queryset=Junior.objects.all())
        return context

    def post(self, request, *args, **kwargs):
        instance=Junior.objects.get(slug=kwargs['jun_slug'])
        form = JunUpdatingForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('profile', jun_slug=kwargs['jun_slug'])
        else:
            form = JunUpdatingForm()
        return redirect('update')

    # def get_object(self, queryset=None):
    #     try:
    #         return queryset.get(slug=self.request.user.juniors.slug)
    #     except Exception as e:
    #         print(e)
    #     return queryset.get(id=self.request.user.pk)



class RegisterJunior(CreateView):
    form_class = UserRegForm
    template_name = 'juniors/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Страница регистрации'
        context['search'] = SearchFilter(self.request.GET, queryset=Junior.objects.all())
        return context

    def post(self, request, *args, **kwargs):
        form = UserRegForm(request.POST)
        if form.is_valid():
            user = form.save()
            slug = slugify(user.username)
            Junior.objects.create(username=user, slug=slug)
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user:
                login(request, user)
            return redirect('update', jun_slug=slug)
        else:
            form = UserRegForm()
        return redirect('index')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'juniors/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        context['search'] = SearchFilter(self.request.GET, queryset=Junior.objects.all())
        return context
    def get_success_url(self):
        return reverse_lazy('index')

def userlogout(request):
    logout(request)
    return redirect('index')

def New(UpdateView):
    model = Junior