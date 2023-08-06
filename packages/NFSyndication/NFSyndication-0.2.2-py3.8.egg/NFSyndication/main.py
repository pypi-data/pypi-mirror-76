#!/usr/bin/env python
# coding=utf8
import collections
from datetime import datetime, timedelta
import time
import configparser
import feedparser
import jinja2
import pytz

from NFSyndication.extras import normalise_post

config = configparser.ConfigParser()
# Get a list of feed URLs
with open('feeds.txt') as f:
    SUBSCRIPTIONS = list(f)

# Date and time setup. I want only posts from "today" and "yesterday",
# where the day lasts until 2 AM.
TIMEZONE = config.get(section='default', option='timezone', fallback='GMT')

# Get the current time in the home timezone, then step back to include
# the last two days.
home_tz = pytz.timezone(TIMEZONE)
dt = datetime.now(home_tz)
if dt.hour < 2:
    dt -= timedelta(hours=72)
else:
    dt -= timedelta(hours=48)
start = dt.replace(hour=0, minute=0, second=0, microsecond=0)

# Convert this time back into UTC.
utc = pytz.utc
START = start.astimezone(utc)


Post = collections.namedtuple('Post', [
    'time',
    'blog',
    'title',
    'author',
    'link',
    'body'
])

def process_entry(entry, blog):
    """
    Coerces an entry from feedparser into a Post tuple.
    Returns None if the entry should be excluded.
    """
    # Get the date of the post.  If it was published more than two days
    # ago, drop the entry.
    try:
        when = entry['updated_parsed']
    except KeyError:
        when = entry['published_parsed']
    when = utc.localize(datetime.fromtimestamp(time.mktime(when)))

    if when < START:
        return

    title = entry['title']
    try:
        author = entry['author']
    except KeyError:
        author = ', '.join(a['name'] for a in entry.get('authors', []))
    link = entry['link']
    try:
        body = entry['content'][0]['value']
    except KeyError:
        body = entry['summary']

    return normalise_post(Post(when, blog, title, author, link, body))


posts = []
for url in SUBSCRIPTIONS:
    feed = feedparser.parse(url)
    try:
        blog = feed['feed']['title']
    except KeyError:
        continue
    for entry in feed['entries']:
        post = process_entry(entry, blog)
        if post:
            posts.append(post)
# Get the template, and drop in the posts
with open('C:/Users/HP 9/AppData/Local/Programs/Python/Python38/lib/site-packages/NFSyndication/templates/template.html', encoding='utf8') as f:
    template = jinja2.Template(f.read())

with open(f'output/index.html', 'w', encoding='utf8') as f:
    f.write(template.render(posts=posts, time=datetime.now()))
