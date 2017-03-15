from __future__ import absolute_import, unicode_literals

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from blog.models import BlogPage


class HomePage(Page):

    def blogs(self):
        # Get list of live blog pages
        blogs = BlogPage.objects.all()

        # Order by most recent date first
        blogs = blogs.order_by('date')

        return blogs
