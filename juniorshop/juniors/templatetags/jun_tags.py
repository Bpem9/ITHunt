from django import template
from juniors.models import *
from itertools import chain
from random import choices, shuffle
from juniors.filters import *
from django.db.models import Min, Max

register = template.Library()

@register.simple_tag()
def get_position():
    return Position.objects.all()

@register.simple_tag(takes_context=True)
def get_juns_tools(context):
    junior = context['junior']
    return junior.tools_set.all()
@register.simple_tag(takes_context=True)
def get_juns_softskills(context):
    junior = context['junior']
    return junior.softskills_set.all()
@register.simple_tag(takes_context=True)
def get_juns_hardskills(context):
    junior = context['junior']
    return junior.hardskills_set.all()

@register.inclusion_tag('juniors/inclusion/messangers_icons.html')
def messangers_icons(jun_slug):
    junior = Junior.objects.get(slug=jun_slug)
    return {'junior': junior}

@register.inclusion_tag('juniors/inclusion/softskill_filters.html')
def filter_softskills(softskills_a=None):
    softskills = SoftSkills.objects.all()[:4]
    return {'softskills': softskills, 'softskills_a': softskills_a}

@register.inclusion_tag('juniors/inclusion/hardskill_filters.html')
def filter_hardskills(hardskills_a=None):
    hardskills = Hardskills.objects.all()[:4]
    return {'hardskills': hardskills, 'hardskills_a': hardskills_a}

@register.inclusion_tag('juniors/inclusion/tools_filters.html')
def filter_tools(tools_a=None):
    tools = Tools.objects.all()[:4]
    return {'tools': tools, 'tools_a': tools_a}

@register.inclusion_tag('juniors/inclusion/salary_range_filter.html')
def salary_range_filter():
    juniors = Junior.objects.all()
    salary_filter = SalaryFilter({'salary_min': 500, 'salary_max': 1000}, juniors)
    minMaxSal = Junior.objects.aggregate(Min('salary'), Max('salary'))
    return {'minSal': minMaxSal['salary__min'], 'maxSal': minMaxSal['salary__max']}

@register.inclusion_tag('juniors/inclusion/cardskillsquery.html')
def cardskillsquery(j):
    hardskills = Hardskills.objects.filter(jun=j)
    softskills = SoftSkills.objects.filter(jun=j)
    tools = Tools.objects.filter(jun=j)
    cardskills = list(chain(hardskills, softskills, tools))
    if len(cardskills) >= 4:
        shuffle(cardskills)
    return {'cardskills': cardskills[:4]}