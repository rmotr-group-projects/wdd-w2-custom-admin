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
        form = SelectBlogForm()
        from pprint import pprint
        print(request.POST)
        pprint(request.POST)
        print('apply' in request.POST)
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        print(selected)
        form = SelectBlogForm(
            initial={
                '_selected_action': selected
                                    }
        )

        # return redirect(request.get_full_path())
        context = {'form': form}
        return render(request, 'entries/admin/change_blog.html', context)
