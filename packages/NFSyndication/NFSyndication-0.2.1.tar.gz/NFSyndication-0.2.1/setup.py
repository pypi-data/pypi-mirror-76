from setuptools import setup, find_packages
from NFSyndication import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name = "NFSyndication",
    version = __version__,
    packages = find_packages(),
    entry_points = {
        'console_scripts': [ 'nfsyndication-src = NFSyndication.main:process_entry' ]
        },
    package_data = {'NFSyndication': ['templates/*.html']},
    description= "News Feed Syndication - A package that read and fetch RSS feeds from the publications.",
    long_description=long_description,
    author = "Web SRC",
    author_email = "web.system.management@gmail.com",
    long_description_content_type="text/markdown",
    license = "GNU GPL",
    keywords = "rss, news",
)
