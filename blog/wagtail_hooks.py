from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from blog.models import Category, BlogAuthor, BlogPage


class CategoryAdmin(ModelAdmin):
    model = Category
    menu_label = 'Blog Categories'  # ditch this to use verbose_name_plural from model
    menu_icon = 'tag'  # change as required
    list_display = ('name',)
    search_fields = ('name',)


class BlogAuthorAdmin(ModelAdmin):
    model = BlogAuthor
    menu_icon = 'user'  # change as required
    list_display = ('name', 'orcid',)
    search_fields = ('name', 'orcid',)


class BlogPageAdmin(ModelAdmin):
    model = BlogPage
    menu_icon = 'doc-empty'
    list_display = ('title', 'locale', 'date', 'full_url', 'teaser')
    ordering = ['-date']


class RegisterGroup(ModelAdminGroup):
    menu_label = 'Blog'
    menu_icon = 'doc-full'  # change as required
    menu_order = 200  # will put in 5th place (000 being 1st, 100 2nd)
    items = (CategoryAdmin, BlogAuthorAdmin, BlogPageAdmin,)


# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(RegisterGroup)
