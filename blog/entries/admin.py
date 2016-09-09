from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import redirect, render
from easy_select2 import select2_modelform

from entries.forms import SelectBlogForm
from entries.models import Author, Blog, Entry

EntryForm = select2_modelform(Entry, attrs={'width': '250px'})


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')

    def get_urls(self):
        urls = super(BlogAdmin, self).get_urls()
        my_urls = [
            url(r'^statistics$', self.statistics),
        ]
        return my_urls + urls

    def statistics(self, request):
        context = {'blogs': Blog.objects.all()}
        return render(request, 'entries/admin/statistics.html', context)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'nationality')
    search_fields = ('id', 'name')


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog', 'headline', 'number_comments', 'scoring')
    list_filter = ('blog',)
    actions = ['reset_scoring', 'change_blog']
    form = EntryForm

    def reset_scoring(self, request, queryset):
        rows_updated = queryset.update(scoring=0)
        self.message_user(request, '{} entry score(s) reset.'.format(rows_updated))

    def change_blog(self, request, queryset):
        print(request.POST)
        if 'apply' in request.POST:
            form = SelectBlogForm(request.POST)
            if form.is_valid():
                queryset.update(blog=form.cleaned_data['blog'])
                self.message_user(request, 'Entries\' blogs updated!')
                return redirect(request.path)
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        form = SelectBlogForm(
            initial={
                '_selected_action': selected
            }
        )
        context = {'form': form}
        return render(request, 'entries/admin/change_blog.html', context)
