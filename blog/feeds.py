from django.contrib.syndication.views import Feed
from blog.models import BlogPage
from django.utils.feedgenerator import Atom1Feed


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

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.teaser

    def item_link(self, item):
        return item.get_full_url()

    def item_pubdate(self, item):
        return item.first_published_at

    def item_updatedate(self, item):
        return item.last_published_at

    def item_categories(self, item):
        return item.categories.all()


class AtomFeed(RssFeed):
    feed_type = Atom1Feed
    link = "/atom"
    subtitle = RssFeed.description
