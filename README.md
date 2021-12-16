# wagtail_blog

This is a Wagtail CMS App that implements a simple (scientific) blog. It implements tags, categories, multiple authors (currently without a bio-page) and blog articles featuring Wagtails Stream Fields, allowing for multiple content blocks, headings and more. It was developed for the [Specialised Information Service for African Studies](https://africanstudieslibrary.org) and is published here for reuse.

# Installation

Clone this repository and copy over the ```blog``` directory into your project.

Enable the app by adding ```blog``` to your ```INSTALLED_APPLICATIONS``` in your settings like so:

```python
INSTALLED_APPS = [
    ...
    'blog',
    ...,
    'wagtail_localize',
    'wagtail_localize.locales',
    'django_social_share',
```

Since this app implements a multilingual blog and enables sharing articles on facebook and twitter ```'wagtail_localize',
    'wagtail_localize.locales'``` and ```django_social_share``` are dependencies needed for the blog to work.

Run ```python manage.py makemigrations``` to create the necessary migrations for the blog and ```python manage.py migrate``` to create all neccesary tables in your database.

# Templates and SCSS

This blogging app comes with templates for an index page and individual articles. The design follows that of the [Specialised Information Service for African Studies](https://africanstudieslibrary.org), so you may want to implement your own projects design. The colour scheme and images have been removed for your convenience.

*It relies on Bootstrap version 5.*

# RSS Feed

This app comes with its own RSS feed. It can be found at ```<your base url>/<your blog>/rss``` or ```<your base url>/<your blog>/atom``` respectively. Some configuration is needed to fit it to your own blog. You need to edit ```blog/feeds.py``` to reflect your blog.

```python
class RssFeed(Feed):
    title = 'Your Blog title'
    link = '/'
    description = "Your Blog description"
    feed_url = '/rss'
    author_name = 'Your Author name'
    categories = ('some', 'categories', 'for', 'your', 'blog')
    feed_copyright = 'CC-BY-SA'
    
    language = 'en'

    def items(self):
        return BlogPage.objects.public().live().filter(locale__language_code='en').order_by('-date')[:50]

    ...
```

As you can see, the default language for this app is English (en). Change this to reflect your primary locale. If you also want to have more than the 50 latest articles in your feed, change this file accordingly.

# Wagtail CMS Backend

This app implements a menu in the Wagtail CMS that allows to easily add new blog articles, authors and categories from a single menu. It's implemented as a register group, so all menus are neatly grouped together for ease of use.

# Dependencies

As stated earlier, this app relies on existing Django and Wagtail Apps to work. These are:

- [Wagtail Localize](https://www.wagtail-localize.org/)
- [Django Social Share](https://pypi.org/project/django-social-share/)

# Environment

This app is tested on:

- Python 3.8, 3.9, 3.10
- Django 3.1, 3.2
- Wagtail 2.13, 2.14, 2.15