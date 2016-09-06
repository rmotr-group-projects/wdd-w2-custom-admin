from datetime import date
from django_webtest import WebTest

from django.test import TestCase
from django.core import urlresolvers
from django.contrib.auth.models import User

from entries.models import Blog, Author, Entry
from tests.fixtures import BlogFactory, AuthorFactory, EntryFactory


class CustomAdminTestCase(WebTest):
    csrf_checks = False

    def setUp(self):
        super(CustomAdminTestCase, self).setUp()
        self.blog_1 = BlogFactory()
        self.blog_2 = BlogFactory()

        self.author = AuthorFactory()

        self.entry_1 = EntryFactory(blog=self.blog_1, scoring=5.55)
        self.entry_1.authors.add(self.author)
        self.entry_1.save()

        self.entry_2 = EntryFactory(blog=self.blog_1)
        self.entry_2.authors.add(self.author)
        self.entry_2.save()

        self.entry_3 = EntryFactory(blog=self.blog_2)
        self.entry_3.authors.add(self.author)
        self.entry_3.save()

        self.user = User.objects.create_user(
            username='User', password='abc123', is_staff=True, is_superuser=True)

    def test_custom_page_with_statistics(self):
        """Should return a template with statistics about the Blogs"""
        response = self.app.get('/admin/entries/blog/statistics/', user=self.user)
        self.assertIn('Number of blogs: 2', str(response.html))
        self.assertIn('{}: 2 entries'.format(self.blog_1.name), str(response.html))
        self.assertIn('{}: 1 entries'.format(self.blog_2.name), str(response.html))

    def test_custom_action_reset_scoring(self):
        """Should reset scoring to zero for given entries"""
        # Preconditions
        self.assertEqual(self.entry_1.scoring, 5.55)

        change_url = urlresolvers.reverse('admin:entries_entry_changelist')
        fixtures = [self.entry_1]
        data = {'action': 'reset_scoring',
                '_selected_action': [f.pk for f in fixtures]}
        self.app.post(change_url, data, user=self.user)

        # Postconditions
        entry = Entry.objects.get(id=self.entry_1.id)
        self.assertEqual(entry.scoring, 0.00)

    def test_custom_action_change_blog(self):
        """Should move given entries from one blog to another"""
        # Preconditions
        self.assertEqual(self.entry_1.blog, self.blog_1)

        change_url = urlresolvers.reverse('admin:entries_entry_changelist')
        fixtures = [self.entry_1]
        data = {'action': 'change_blog',
                '_selected_action': [f.pk for f in fixtures]}
        response = self.app.post(change_url, data, user=self.user)
        form = response.form
        form['blog'] = "2"
        form.submit('apply')

        # Postconditions
        entry = Entry.objects.get(id=self.entry_1.id)
        self.assertEqual(entry.blog, self.blog_2)

    def test_select2(self):
        """Should successfully import any Select2 external library in django admin"""
        response = self.app.get('/admin/entries/entry/add/', user=self.user)
        self.assertIn('select2', str(response.html))

    def test_custom_login(self):
        """Should add a custom button to django admin login template"""
        response = self.app.get('/admin/login/')
        self.assertIn('Log in with Github', str(response.html))
