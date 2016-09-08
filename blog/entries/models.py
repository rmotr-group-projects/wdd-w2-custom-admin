
from __future__ import unicode_literals

from django.db import models


COUNTRY_CHOICES = (
    ('ar', 'Argentina'),
    ('us', 'United States'),
    ('de', 'Germany'),
    ('br', 'Brazil'),
    ('fr', 'France')
)


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __unicode__(self):
        return self.name

    __str__ = __unicode__


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    nationality = models.CharField(max_length=2, choices=COUNTRY_CHOICES)

    def __unicode__(self):
        return self.name

    __str__ = __unicode__


class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)
    authors = models.ManyToManyField(Author)
    number_comments = models.IntegerField()
    scoring = models.DecimalField(max_digits=3, decimal_places=2)

    def __unicode__(self):
        return self.headline

    __str__ = __unicode__
    
    class Meta:
        verbose_name_plural = 'entries'
