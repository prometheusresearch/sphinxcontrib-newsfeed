*****************************************************
  ``sphinxcontrib-blog`` -- A Sphinx Blog Extension
*****************************************************

Overview
========

``sphinxcontrib-blog`` is a extension for adding a simple *Blog*, *News*
or *Announcements*  section to a Sphinx_ website.

Features:

* Makes blog posts from Sphinx documents.
* Generates a list of blog posts with teasers and an RSS feed.
* Supports comments via Disqus_.

You can see this extension in action at http://htsql.org/blog/.

This software is written by Kirill Simonov (`Prometheus Research, LLC`_)
and released under BSD license.


Usage
=====

To use this extension with your Sphinx website, add the following line
to ``conf.py``::

    extensions.append('sphinxcontrib.blog')

To enable comments, you also need to specify the Disqus_ website
identifier::

    disqus_shortname = '...'

Now you can make a blog post from any Sphinx document by adding
directive ``blogpost``.  For example::

    First Post!!!
    =============

    .. blogpost::
       :date: 2013-01-01

    Welcome to my new blog!!!

Use ``blogcut`` directive to separate the post teaser from the content::

    Post with a Teaser
    ==================

    .. blogpost::
       :date: 2013-02-02

    Place summary here.

    .. blogcut::

    Here is the main body of the post.

To make a list of blog posts and generate an RSS feed, use ``blogtree``
directive::

    .. blogtree::
       :rss: index.rss
       :title: My Project News

       with-teaser
       first-post

The ``blogtree`` body should contain a list of documents (just like
``toctree``).

The ``blogtree`` options specify the name of the RSS feed file and RSS
metadata.  You need to manually add a link to the RSS feed to your
templates::

      <link rel="alternate"
            type="application/rss+xml"
            title="My Project News"
            href="/index.rss" />


Reference
=========

Directives
----------

``blogpost``
    Inserts the post metadata.

    This directive has no body.

    Options:

    ``author``
        The author of the post (optional).
    ``date``
        The date of the post in ``YYYY-MM-DD`` format.

``blogtree``
    Inserts a list of blog posts with teasers at the current location.

    This directive should contain a list of document names (similar to
    ``toctree``).

    Options:

    ``rss``
        Where to write the RSS feed (optional).
    ``title``
        The name of the blog (for RSS metadata).
    ``description``
        The description of the blog (for RSS metadata).
    ``link``
        The URL of the blog (for RSS metadata).

``blogcut``
    Separates the post teaser from the main body of the post.

    This directive has no options and no body.

``disqus``
    Inserts a Disqus_ comment widget.

    Normally you don't need to use this directive since if
    ``disqus_shortname`` parameter is set, Disqus comments are included
    automatically with every blog post.  This directive allows you to
    use Disqus with regular Sphinx documents.

    Options:

    ``shortname``
        The website identifier.  Use to override ``disqus_shortname``
        configuration parameter.
    ``identifier``
        The page identifier.  If not set, use the document name.
    ``title``
        The title of the page.  If not set, use the document title.

Configuration parameters
------------------------

``disqus_shortname``
    Sets the unique identifier for a Disqus website.  To acquire one, you
    need to register the website on http://disqus.com/.

``disqus_developer``
    Sets the developer mode (``False`` or ``True``).

CSS classes
-----------

``blog-meta``
    Wraps for the post metadata block.

``blog-author``
    Wraps the author name.

``blog-date``
    Wraps the post date.

``blog-disqus``
    Wraps the Disqus comment widget.

``blog-ref``
    Wraps the post title in the list of posts.

``blog-more``
    Wraps the *Read more...* link.


.. _Sphinx: http://sphinx-doc.org/
.. _Disqus: http://disqus.org/
.. _Prometheus Research, LLC: http://prometheusresearch.com/


.. vim: set spell spelllang=en textwidth=72:
