from django.contrib import admin
from django.shortcuts import render, redirect
from entries.models import Blog, Author, Entry
from entries.forms import SelectBlogForm


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'nationality')
    search_fields = ('id', 'name')


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog', 'headline', 'number_comments', 'scoring')
    list_filter = ('blog',)
    actions = ['reset_scoring', 'change_blog']

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
