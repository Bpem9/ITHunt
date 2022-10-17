from django.db.models import Q
from .filters import SearchFilter
from .models import Junior


class SkillsFilters:
    def get_filtrated_queryset(self, **kwargs):
        if 'pos_slug' in kwargs.keys():
            juniors = Junior.objects.filter(position__slug=kwargs['pos_slug'])
        else:
            juniors = Junior.objects.all()
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

    # def get_sorted_queryset(self, **kwargs):
    #     return juniors.sorted()
    # ''' Стартовая выборка - все джуны из БД.
    #      Если метод GET что-то возвращает - все значения записываются в виде списка скиллов в skfl, hkdl или tlls.
    #      В новую выборку джунов отфильтовываются джуны из стартовой выборки БД в атрибуте softskills/hardskills/tools__skill
    #      (из вторичной модели softskills, hardskills или tools) которых содержатся скиллы из skfl, hdkl ли tlls.
    #      Список джунов подается в шаблон html. '''