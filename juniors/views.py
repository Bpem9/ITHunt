from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin, ModelFormMixin

from .models import *
from .filters import *
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
        juniors = super().get_filtrated_queryset(**kwargs)
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
    slug_url_kwarg = 'jun_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messengers'] = self.object.owner.values('email', 'website', 'whatsup', 'viber', 'facebook',
                                                         'vk', 'instagram', 'behance', 'pinterest')
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


class JuniorUpdate(UpdateView):
    model = Junior
    form_class = JunUpdatingForm
    template_name = 'juniors/profile_update.html'
    slug_url_kwarg = 'jun_slug'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = SearchFilter(self.request.GET, queryset=Junior.objects.all())
        instance, _ = Messengers.objects.get_or_create(junior=self.request.user.junior)
        context['messengers_form'] = MessengersForm(instance=instance)
        return context

    def post(self, request, *args, **kwargs):
        super().post(self, request, *args, **kwargs)
        instance, _ = Messengers.objects.get_or_create(junior=self.request.user.junior)
        messengers_form = MessengersForm(request.POST, instance=instance)
        if messengers_form.is_valid():
            messengers = messengers_form.save(commit=False)
            if messengers.email:
                if 'mailto:' not in messengers.email:
                    messengers.email = 'mailto:' + messengers.email
            if messengers.website:
                if 'https://' not in messengers.website:
                    messengers.website = 'https://' + messengers.website
            messengers.junior = self.get_object()
            messengers.save()
            return redirect('profile', jun_slug=kwargs['jun_slug'])
        form = MessengersForm()
        return redirect('update', jun_slug=kwargs['jun_slug'])

    def get_success_url(self):
        return reverse('profile', kwargs={'jun_slug': self.object.slug})


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
            next_id=Junior.objects.aggregate(Max('id'))['id__max'] + 1
            Junior(id=next_id, username=user, slug=slug).save()
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user:
                login(request, user)
            return redirect('update', jun_slug=slug)
        else:
            form = UserRegForm()
        return redirect('registration')

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