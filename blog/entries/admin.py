from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from easy_select2 import select2_modelform

from entries.models import Blog, Author, Entry
from entries.forms import SelectBlogForm


class BaseApplicationAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(BaseApplicationAdmin, self).get_urls()
        my_urls = [
            url(r'^statistics/$',
                self.admin_site.admin_view(self.statistics)),
        ]
        return my_urls + urls

    def statistics(self, request):
        blogs_entries_count = {}
        for blog in Blog.objects.all():
            blogs_entries_count[blog.name] = Entry.objects.filter(blog=blog).count()
        blogs_entries_count = sorted(blogs_entries_count.items(), key=lambda x: -x[1])

        context = {}
        context.update({
            'blogs': Blog.objects.count(),
            'blogs_entries_count': blogs_entries_count
        })
        return TemplateResponse(request, "admin/statistics.html", context)


@admin.register(Blog)
class BlogAdmin(BaseApplicationAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'nationality')
    search_fields = ('id', 'name')


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    form = select2_modelform(Entry, attrs={'width': '600px'})
    list_display = ('id', 'blog', 'headline', 'number_comments', 'scoring')
    list_filter = ('blog',)
    search_fields = ('id', 'blog', 'authors')
    actions = ['reset_scoring', 'change_blog']

    def reset_scoring(self, request, queryset):
        for obj in queryset:
            obj.scoring = 0
            obj.save()

        self.message_user(request, "Scoring resetted")

    reset_scoring.short_description = ("Reset scoring")

    def change_blog(self, request, queryset):
        if 'apply' in request.POST:
            form = SelectBlogForm(request.POST)
            if form.is_valid():
                instance = form.cleaned_data['blog']
                for entry in queryset:
                    entry.blog = instance
                    entry.save()
                self.message_user(
                    request, "Successfully changed blog for {} entries.".format(queryset.count()))
                return HttpResponseRedirect(request.get_full_path())
        else:
            form = SelectBlogForm(
                initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        return render(
            request,
            'admin/change_blog.html',
            context={'instances': queryset, 'form': form})

    change_blog.short_description = ("Change blog")
