from django.db import models
from django import forms
from django_extensions.db.fields import AutoSlugField

from wagtail.core.models import Page

from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock

from taggit.models import TaggedItemBase

from modelcluster.fields import ParentalManyToManyField, ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = AutoSlugField(populate_from='name', verbose_name='Slug (Leave empty for autogeneration)', editable=True)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ['name']


class BlogAuthor(models.Model):
    name = models.CharField(max_length=150)
    orcid = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='name', verbose_name='Slug (Leave empty for autogeneration)', editable=True)
    portrait = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    portrait_alt_text = models.CharField(max_length=3000, blank=False, default='A stylized icon for a person.')
    biography = RichTextField()

    panels = [
        ImageChooserPanel("portrait"),
        FieldPanel('portrait_alt_text'),
        FieldPanel('name'),
        FieldPanel('biography'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Post Author"
        verbose_name_plural = "Blog Post Authors"
        ordering = ['name']


class BlogIndex(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = [
        'BlogPage'
    ]
    max_count = 1

    bannertext = models.CharField(max_length=255, blank=False, default='Welcome to our Blog')

    content_panels = Page.content_panels + [
        FieldPanel('bannertext'),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # Add extra variables and return the updated context
        filter_cat = request.GET.get('categories', None)
        query = request.GET.get('query', None)
        tags = request.GET.get('tags', None)

        if query == '':
            query = None

        if query is not None:
            context['query'] = query
            if query is not None:
                if ' ' in query:
                    query = query.split(' ')
                else:
                    query = [query]

                q = models.Q()
                for item in query:
                    q |= models.Q(teaser__search=item) | models.Q(categories__name__unaccent__trigram_similar=item) | models.Q(tags__name__unaccent__trigram_similar=item) | models.Q(body__icontains=item)

                entries = BlogPage.objects.child_of(self).live().filter(q).order_by('id').distinct('id')
        else:
            entries = BlogPage.objects.child_of(self).live()

        if filter_cat is not None:
            entries = BlogPage.objects.child_of(self).live().filter(categories__slug=filter_cat)
            context['filtered_cat'] = Category.objects.get(slug=filter_cat)
        
        if tags is not None:
            entries = entries.filter(tags__slug__in=[tags])

        context['blog_entries'] = entries
        # uncomment to activate blog categories again
        # context['blog_categories'] = Category.objects.all()
        return context


class BlogTags(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )


class BlogPage(Page):
    parent_page_types = ['BlogIndex']
    subpage_types = []

    post_author = ParentalManyToManyField('BlogAuthor')
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    teaser = models.CharField(max_length=1500)
    categories = ParentalManyToManyField("Category", blank=True)
    tags = ClusterTaggableManager(through=BlogTags, blank=True)
    banner_image_alt_text = models.CharField(max_length=3000, blank=False, default='This is an alt Text')

    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('sub_heading', blocks.CharBlock(form_classname='sub_heading')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('quote', blocks.BlockQuoteBlock()),
        ('rawHTML', blocks.RawHTMLBlock())
    ])

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('post_author', heading='Please select the authors for this blog post', widget=forms.CheckboxSelectMultiple),
            ImageChooserPanel("banner_image"),
            FieldPanel('banner_image_alt_text'),
            FieldPanel('teaser'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags'),
        ], heading='Blog Data'),
        StreamFieldPanel('body'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['blog_categories'] = Category.objects.all()
        siblings = BlogPage.objects.sibling_of(self).live().public().exclude(slug=self.slug)
        similar_categories = siblings.filter(categories__in=self.categories.all()).distinct()
        similar_tags = siblings.filter(tags__in=self.tags.all()).distinct().distinct()
        context['similar'] = similar_tags.union(similar_categories)
        previous = self.get_prev_sibling()
        if previous is not None:
            context['previous'] = previous.url
        else:
            context['previous'] = '#'
        next_sibling = self.get_next_sibling()
        if next_sibling is not None:
            context['next'] = next_sibling.url
        else:
            context['next'] = '#'

        return context
