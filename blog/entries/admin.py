from django.contrib import admin
from django.conf.urls import patterns
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.db.models import Count
from easy_select2 import select2_modelform

from entries.models import Blog, Author, Entry
from entries.forms import SelectBlogForm

EntryForm = select2_modelform(Entry, attrs={'width': '250px'})


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    
    # Helpful example on extending the admin site with a custom view
    # https://www.stavros.io/posts/how-to-extend-the-django-admin-site-with-custom/
    def get_urls(self):
        urls = super(BlogAdmin, self).get_urls()
        my_urls = patterns('', 
            (r'statistics/$', self.admin_site.admin_view(self.statistics)))
        return my_urls + urls
    
    def statistics(self, request):
        # Query for the statistics to display
        blog_count = Blog.objects.count()
        entries_count = Blog.objects.values('name').annotate(Count("entry"))
        context = {
            'blog_count': blog_count,
            'entries_count_by_blog': entries_count
        }
        return render(request, 'admin/entries/statistics.html', context=context)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'nationality')
    search_fields = ('id', 'name')


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog', 'headline', 'number_comments', 'scoring')
    list_filter = ('blog',)
    form = EntryForm
    
    # Docs on adding actions
    # https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.ModelAdmin
    
    actions = ['reset_scoring', 'change_blog']
    
    def reset_scoring(self, request, queryset):
        entries_updated = queryset.update(scoring=0)
        if entries_updated:
            self.message_user(request, "Scoring was reset")
    
    
    def change_blog(self, request, queryset):
        # If it is submission of the new blog selection, update the entries;
        #  otherwise, just render the form.
        if 'apply' in request.POST:
            form = SelectBlogForm(request.POST)
            if form.is_valid():
                # Move all the entries to the selected blog
                blog_instance = form.cleaned_data['blog']
                for entry in queryset:
                    entry.blog = blog_instance
                    entry.save()
                    
                self.message_user(
                    request, 
                    "Blog updated for {} entries".format(queryset.count())
                )
                return HttpResponseRedirect(request.get_full_path())
        
        else:
            # Get a list of the selected entries
            selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
            
            # Initialize the form, with the selected entries in hidden inputs
            form = SelectBlogForm(
                initial={
                    '_selected_action': selected
                }
            )
        
        context = {'form': form}
        return render(request, 'admin/entries/change_blog.html', context=context)