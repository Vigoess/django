from django.contrib import admin

# Register your models here.
from booktest.models import NewsInfo, TypeInfo

class NewsInfomanager(admin.ModelAdmin):
    list_display = ['id','ntitle','ncontent','npub_date']

class TypeInfomanager(admin.ModelAdmin):
    list_display = ['id','tname']



admin.site.register(NewsInfo,NewsInfomanager)
admin.site.register(TypeInfo,TypeInfomanager)