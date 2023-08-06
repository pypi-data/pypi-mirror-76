# About the News Feed Python

This is a set of scripts for aggregating RSS feeds.  

## Installation

You can install package through the line command
     
 `pip install NFSyndication`

Put a list of feed URLs in `feeds.txt`.  One feed per line.  Run the command:

 `nfsyndication-src`

Assuming nothing goes wrong, the posts will be written to `.html` file.

## Bug fix
After many hours of working to development, it was set up an way of path configuration due to errors. <br>
Meanwhile, we have to set code `os.path.dirname(os.path.realpath(__file__))` with the globalization of variables for source code regarding `main.py` file.

