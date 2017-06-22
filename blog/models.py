from __future__ import absolute_import, unicode_literals

from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


# Create your models here.
class BlogPage(Page):

    # Database fields

    body = RichTextField()
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body', classname="full"),
        InlinePanel('related_links', label="Related Links")
    ]


class BlogPageRelatedLink(Orderable):
    page = ParentalKey(BlogPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro')
    ]

    @property
    def blogs(self):
        # Get list of live blog pages that are descendents of this page
        blogs = BlogPage.objects.live().descendent_of(self)

        # Order by most recent date
        blogs = blogs.order_by('date')

        return blogs

    def get_context(self, request):
        # Get blogs
        blogs = self.blogs

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            blogs = blogs.filter(tags__name=tag)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(blogs, 5)  # Show 5 blogs per page
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        # Update template context
        context = super(BlogIndexPage, self).get_context(request)
        context['blogs'] = blogs
        return context

    def get_sitemap_urls(self):
        return [
            {
                'location': self.full_url,
                'lastmod': self.latest_revision_created_at,
                'changefreq': 'monthly',
                'priority': .5
            }
        ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
    ]

    promote_panels = Page.promote_panels
