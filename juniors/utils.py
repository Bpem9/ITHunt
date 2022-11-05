from django.db.models import Q
from .filters import SearchFilter
from .models import *


class SkillsFilters:
    def get_filtrated_queryset(self, **kwargs):
        if 'pos_slug' in kwargs.keys():
            juniors = Junior.objects.filter(position__slug=kwargs['pos_slug'])
        else:
            juniors = Junior.objects.exclude(position__slug='client')
        search = SearchFilter(self.request.GET, queryset=juniors)
        sfkl = self.request.GET.getlist('softskills')
        hdkl = self.request.GET.getlist('hardskills')
        tlls = self.request.GET.getlist('tools')
        flts = [*sfkl, *hdkl, *tlls]
        if search.qs:
            juniors = search.qs
        if flts:
            juniors = juniors.filter(Q(softskills__skill__in=flts) |
                                     Q(hardskills__skill__in=flts) |
                                     Q(tools__tool__in=flts)
                                     )
        return juniors.distinct()

    def get_sorted_queryset(self, juniors, **kwargs):
        if self.request.GET.get('sort') == 'По алфавиту':
            juniors = juniors.order_by('first_name', 'last_name')
        # if self.request.GET.get('sort') == 'По рейтингу':
        #     juniors = juniors.sorted('position')
        if self.request.GET.get('sort') == 'По зарплате':
            juniors = juniors.order_by('salary')
        if self.request.GET.get('sort') == 'По локации':
            juniors = juniors.order_by('country__country')
        return juniors
    # ''' Стартовая выборка - все джуны из БД.
    #      Если метод GET что-то возвращает - все значения записываются в виде списка скиллов в skfl, hkdl или tlls.
    #      В новую выборку джунов отфильтовываются джуны из стартовой выборки БД в атрибуте softskills/hardskills/tools__skill
    #      (из вторичной модели softskills, hardskills или tools) которых содержатся скиллы из skfl, hdkl ли tlls.
    #      Список джунов подается в шаблон html. '''


class SkillControl:
    def _get_hardskills_instance(self, request, *args, **kwargs):
        model = JuniorHardskills
        hardskill = Hardskills.objects.get(skill=request.request.GET.get('skill'))
        instance = (model, hardskill)
        return instance
    def _get_softskills_instance(self, request, *args, **kwargs):
        model = JuniorSoftskills
        softskill = SoftSkills.objects.get(skill=request.request.GET.get('skill'))
        instance = (model, softskill)
        return instance
    def _get_tools_instance(self, request, *args, **kwargs):
        model = JuniorTools
        tool = Tools.objects.get(tool=request.request.GET.get('skill'))
        instance = (model, tool)
        return instance

    def _add_skill(self, request, *args, **kwargs):
        junior = request.request.user.junior
        if request.request.GET.get('t') == 'hardskill':
            instance = self._get_hardskills_instance(request, *args, **kwargs)
        if request.request.GET.get('t') == 'softskill':
            instance = self._get_softskills_instance(request, *args, **kwargs)
        if request.request.GET.get('t') == 'tool':
            instance = self._get_tools_instance(request, *args, **kwargs)
        model, skill = instance
        model(junior=junior, skill=skill).save()

    def _del_skill(self, request, *args, **kwargs):
        junior = request.request.user.junior
        if request.request.GET.get('t') == 'hardskill':
            instance = self._get_hardskills_instance(request, *args, **kwargs)
        if request.request.GET.get('t') == 'softskill':
            instance = self._get_softskills_instance(request, *args, **kwargs)
        if request.request.GET.get('t') == 'tool':
            instance = self._get_tools_instance(request, *args, **kwargs)
        model, skill = instance
        model.objects.get(junior=junior, skill=skill).delete()
