from django.contrib import admin
from .models import *

class JuniorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'url_img', 'position', 'exp', 'country', 'salary')
    # list_display_links = ('id', 'fio', 'exp', 'salary', 'cat')
    search_fields = ('first_name', 'last_name')
    list_filter = ('position', )
    list_editable = ('first_name', 'exp', 'country', 'position', 'username', 'salary')
    prepopulated_fields = {'slug': ('last_name',)}

class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'slug')
    list_display_links = ('id', 'position')
    search_fields = ('position',)
    prepopulated_fields = {"slug": ("position", )}

class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'image')
    list_display_links = ('id', 'country', 'image')
    prepopulated_fields = {"slug": ("country",)}

class SoftingAdmin(admin.ModelAdmin):
    pass

class ToolingAdmin(admin.ModelAdmin):
    pass

class HardingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Junior, JuniorAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(SoftSkills)
admin.site.register(JuniorSoftskills, SoftingAdmin)

admin.site.register(Tools)
admin.site.register(JuniorTools, ToolingAdmin)

admin.site.register(Hardskills)
admin.site.register(JuniorHardskills, HardingAdmin)
