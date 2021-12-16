from django.urls import path

from blog.feeds import RssFeed,AtomFeed

urlpatterns = [
	path(r'rss',RssFeed(), name='rssfeed'),
	path(r'atom',AtomFeed(), name='atomfeed')
]