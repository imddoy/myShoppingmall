from django.contrib import admin
from .models import Item, Category, Company, Tag
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.
admin.site.register(Item, MarkdownxModelAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)

class CompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Company, CompanyAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name', )}

admin.site.register(Tag, TagAdmin)