from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin, ModelFormMixin

from .models import *
from .filters import *
from .GdrvtoSQL.stuff import lst_juns, hrds, tolls, sfts, poss, countries
from slugify import slugify
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import *
from .utils import SkillsFilters




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


class JuniorProfile(ModelFormMixin, DetailView):
    model = Junior
    form_class = JunUpdatingForm
    template_name = 'juniors/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        context['search'] = SearchFilter(self.request.GET, queryset=Junior.objects.all())
        context['softskillsup'] = SoftSkillsUpdate
        context['hardskillup'] = HardskillsUpdate
        context['toolsup'] = ToolsUpdate
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('first_name'):
            jun = Junior.objects.get(slug=request.user.junior.slug)
            form = JunUpdatingForm(request.POST, instance=jun)
            if form.is_valid():
                form.save()
                return redirect('profile')
            else:
                print('='*10, form.errors, '='*10)
                return redirect('profile')

        if request.POST.get('hardskill'):
            instance = JuniorHardskills(junior=self.request.user.junior, hardskill=Hardskills.objects.get(id=self.request.POST.get('hardskill')))
            form = HardskillsUpdate(self.request.POST, instance=instance)
            print(form.errors)
            if form.is_valid():
                try:
                    form.save()
                except Exception as e:
                    form.add_error(None, e.__cause__)
                finally:
                    return redirect('profile')
        elif request.POST.get('softskill'):
            instance = JuniorSoftskills(junior=self.request.user.junior, softskill=SoftSkills.objects.get(id=self.request.POST.get('softskill')))
            form = SoftSkillsUpdate(request.POST, instance=instance)
            if form.is_valid():
                try:
                    form.save()
                    return redirect('profile')
                except Exception as e:
                    form.add_error(None, e.__cause__)
                finally:
                    return redirect('profile')
            else:
                return redirect('profile')
        elif request.POST.get('tool'):
            instance = JuniorTools(junior=self.request.user.junior, tool=Tools.objects.get(id=self.request.POST.get('tool')))
            form = ToolsUpdate(self.request.POST, instance=instance)
            print(form.errors)
            if form.is_valid():
                try:
                    form.save()
                    return redirect('profile')
                except Exception as e:
                    form.add_error(None, e.__cause__)
                finally:
                    return redirect('profile')
            else:
                return redirect('profile')

        elif request.POST.get('del'):
            print('del работает')
            return render(HttpResponse('del работает'))

    def get_initial(self):
        initial = super().get_initial()
        jun = self.request.user.junior
        initial['first_name'] = jun.first_name
        initial['last_name'] = jun.last_name
        initial['position'] = jun.position
        initial['description'] = jun.description
        return initial

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
        form = JunUpdatingForm(request.POST)
        if form.is_valid():
            print(form)
            form.save()
        return redirect('profile')


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
            form.save()
            return redirect('profile')
        else:
            form = UserRegForm()


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