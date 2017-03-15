from __future__ import absolute_import, unicode_literals

from wagtail.wagtailcore.models import Page
from blog.models import BlogPage


class HomePage(Page):

    def blogs(self):
        # Get list of live blog pages
        blogs = BlogPage.objects.all()

        # Order by most recent date first
        blogs = blogs.order_by('date')

        return blogs
