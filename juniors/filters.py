import django_filters
from django import forms
from django.db.models import Q
from django_filters import CharFilter, RangeFilter, ChoiceFilter, BooleanFilter

from .models import *

class SalaryFilter(django_filters.FilterSet):
    salary = django_filters.NumericRangeFilter()
    class Meta:
        model = Junior
        fields = ['salary']


class SearchFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='fio',
                                  widget=forms.TextInput(
                                  attrs={'class':"search-form__input",
                                         'placeholder':"Поиск по ключевому слову",
                                         'type':"text"
                                         }
                                    )
                                  )
    class Meta:
        model = Junior
        fields = ['q']

    def fio(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )
