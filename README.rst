****************************************************************
  ``sphinxcontrib-newsfeed`` -- News Feed extension for Sphinx
****************************************************************

Overview
========

``sphinxcontrib-newsfeed`` is a extension for adding a simple *Blog*,
*News* or *Announcements*  section to a Sphinx_ website.

Features:

* Makes feed entries from Sphinx documents.
* Generates a list of entries with teasers.
* Saves the feed to a file in RSS format.
* Supports comments via Disqus_.

You can see this extension in action at http://htsql.org/blog/.

This software is written by Kirill Simonov (`Prometheus Research, LLC`_)
and released under BSD license.


Usage
=====

To enable this extension, add the following line to ``conf.py``::

    extensions.append('sphinxcontrib.newsfeed')

To add a comment form to news entries, you also need to specify the
Disqus_ website identifier::

    disqus_shortname = '...'

Now you can convert any Sphinx document to a news entry by using
directive ``feed-entry``.  For example::

    Welcome!!!
    ==========

    .. feed-entry::
       :date: 2012-01-01

    Welcome to the news feed of **Elvensense**.  Here we will post
    release announcements and other project news.

Use ``cut`` directive to separate the entry teaser from the content::

    Elvensense 96 is released
    =========================

    .. feed-entry::
       :date: 2012-12-31

    We are proud to announce a new release of **Elvensense**.

    .. cut::

    Specific changes since the last release:

    * An exciting feature was added.
    * An annoying bug was fixed.


To make a list of news entries and generate an RSS file, use ``feed``
directive::

    .. feed::
       :rss: index.rss
       :title: Elvensense News

       release
       welcome

The body of ``feed`` directive must list documents containing news
entries (similar to ``toctree``).  The options of ``feed`` directive
define the name of the RSS file and describe the feed metadata.

You need to manually update your HTML templates to add a link to the RSS
feed::

      <link rel="alternate"
            type="application/rss+xml"
            title="Elvensense News"
            href="/index.rss" />


Reference
=========

Directives
----------

``feed-entry``
    Specifies an entry metadata.

    This directive has no body.

    Options:

    ``author``
        The author of the post (optional).
    ``date``
        The date of the post in ``YYYY-MM-DD`` format.

``feed``
    Inserts a list of entries with teasers at the current location.

    This directive should contain a list of document names (similar to
    ``toctree``).  This directive adds the documents to the hierarchy,
    so that you don't need to add the to ``toctree``.

    Options:

    ``rss``
        Where to write the RSS feed (optional).
    ``title``
        The name of the RSS channel.
    ``description``
        Description of the RSS channel.
    ``link``
        The website URL.

``cut``
    Separates the entry teaser from the rest of the text.

    This directive has no options and no body.

``disqus``
    Inserts a Disqus_ comment widget.

    Normally you don't need to use this directive for news entries
    since, if ``disqus_shortname`` parameter is set, Disqus comment form
    is encluded automatically with every feed entry.  This directive
    allows you to use Disqus with regular Sphinx documents.

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

``feed-meta``
    Wraps for the post metadata block.

``feed-author``
    Wraps the author name.

``feed-date``
    Wraps the post date.

``feed-disqus``
    Wraps the Disqus comment widget.

``feed-ref``
    Wraps the post title in the list of posts.

``feed-more``
    Wraps the *Read more...* link.


.. _Sphinx: http://sphinx-doc.org/
.. _Disqus: http://disqus.org/
.. _Prometheus Research, LLC: http://prometheusresearch.com/


.. vim: set spell spelllang=en textwidth=72:
