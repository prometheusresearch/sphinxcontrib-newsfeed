#
# Copyright (c) 2013, Prometheus Research, LLC
#


from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx import addnodes
from sphinx.util import docname_join
import os.path, datetime, re
import PyRSS2Gen


class FeedDirective(Directive):

    has_content = True
    option_spec = {
            'rss': directives.unchanged,
            'atom': directives.unchanged,
            'title': directives.unchanged,
            'link': directives.unchanged,
            'description': directives.unchanged,
    }

    def run(self):
        env = self.state.document.settings.env
        output = []
        entries = []
        includefiles = []
        for entry in self.content:
            if not entry:
                continue
            docname = docname_join(env.docname, entry)
            if docname not in env.found_docs:
                output.append(self.state.document.reporter.warning(
                    'feed contains a reference to nonexisting '
                    'document %r' % docname, line=self.lineno))
                env.note_reread()
            else:
                entries.append((None, docname))
                includefiles.append(docname)
        subnode = addnodes.toctree()
        subnode['parent'] = env.docname
        subnode['entries'] = entries
        subnode['includefiles'] = includefiles
        subnode['maxdepth'] = 1
        subnode['glob'] = False
        subnode['hidden'] = True
        subnode['numbered'] = False
        subnode['titlesonly'] = False
        wrappernode = nodes.compound(classes=['toctree-wrapper'])
        wrappernode.append(subnode)
        output.append(wrappernode)
        subnode = feed()
        subnode['entries'] = includefiles
        subnode['rss'] = self.options.get('rss')
        subnode['atom'] = self.options.get('atom')
        subnode['title'] = self.options.get('title', '')
        subnode['link'] = self.options.get('link', '')
        subnode['description'] = self.options.get('description', '')
        output.append(subnode)
        return output


class FeedEntryDirective(Directive):

    option_spec = {
            'author': directives.unchanged,
            'date': directives.unchanged_required,
    }

    def run(self):
        author = self.options.get('author')
        date = self.options.get('date')
        for format in ["%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"]:
            try:
                date = datetime.datetime.strptime(date, format)
            except ValueError:
                pass
            else:
                break
        else:
            return [doc.reporter.error("invalid date `%s`" % date,
                                       lineno=self.lineno)]
        meta_node = entrymeta(classes=['feed-meta'])
        meta_node += nodes.Text(u'Published')
        if author:
            meta_node += nodes.Text(u' by ')
            author_node = nodes.emphasis(classes=['feed-author'])
            author_node += nodes.Text(author)
            meta_node += author_node
        if date:
            meta_node += nodes.Text(u' on ')
            date_node = nodes.emphasis(classes=['feed-date'])
            if date.time():
                date_node += nodes.Text(date)
            else:
                date_node += nodes.Text(date.date())
            meta_node += date_node
        meta_node['author'] = author
        meta_node['date'] = date
        return [meta_node]


class CutDirective(Directive):

    def run(self):
        return [entrycut()]


class DisqusDirective(Directive):

    option_spec = {
            'shortname': directives.unchanged,
            'identifier': directives.unchanged,
            'title': directives.unchanged,
    }

    def run(self):
        doc = self.state.document
        env = doc.settings.env
        node = disqus(classes=['feed-disqus'])
        if 'shortname' in self.options:
            node['shortname'] = self.options['shortname']
        else:
            if not env.config.disqus_shortname:
                return [doc.reporter.error("config option `disqus_shortname`"
                                           " is not set", lineno=self.lineno)]
            node['shortname'] = env.config.disqus_shortname
        if 'identifier' in self.options:
            node['identifier'] = self.options['identifier']
        else:
            node['identifier'] = "/%s" % env.docname
        node['title'] = self.options.get('title')
        node['developer'] = env.config.disqus_developer
        return [node]


class feed(nodes.General, nodes.Element):
    pass


class entrymeta(nodes.paragraph):
    pass


class entrycut(nodes.General, nodes.Element):
    pass


class disqus(nodes.General, nodes.Element):
    pass


def visit_entrymeta(self, node):
    self.visit_paragraph(node)


def depart_entrymeta(self, node):
    self.depart_paragraph(node)


def visit_entrycut(self, node):
    raise nodes.SkipNode


DISQUS_TEMPLATE = """\
<div id="disqus_thread"></div>
<script type="text/javascript">
%(config)s
(function() {
    var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
    dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
    (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
})();
</script>
<noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
<a href="http://disqus.com" class="dsq-brlink">blog comments powered by <span class="logo-disqus">Disqus</span></a>
"""


def visit_disqus(self, node):
    shortname = node['shortname']
    identifier = node['identifier']
    title = node['title']
    developer = node['developer']
    config = []
    if shortname:
        config.append(('disqus_shortname', shortname))
    if identifier:
        config.append(('disqus_identifier', identifier))
    if title:
        config.append(('disqus_title', title))
    if developer:
        config.append(('disqus_developer', '1'))
    config = "".join("var %s = \"%s\";\n"
                     % (name, value.replace('\\', '\\\\')
                                   .replace('\"', '\\"'))
                     for name, value in config)
    html = DISQUS_TEMPLATE % vars()
    self.body.append(self.starttag(node, 'div'))
    self.body.append(html)
    self.body.append("</div>")
    raise nodes.SkipNode


def process_feed(app, doctree, fromdocname):
    env = app.builder.env
    if env.config.disqus_shortname and doctree.traverse(entrymeta):
        node = disqus(classes=['feed-disqus'])
        node['shortname'] = env.config.disqus_shortname
        node['identifier'] = "/%s" % fromdocname
        node['title'] = env.titles[fromdocname][0]
        node['developer'] = env.config.disqus_developer
        doctree += node
    for node in doctree.traverse(feed):
        rss_output = node['rss']
        rss_title = node['title']
        rss_link = node['link']
        rss_description = node['description']
        rss_items = []
        replacement = []
        for docname in node['entries']:
            entry = env.get_doctree(docname)
            for meta in entry.traverse(entrymeta):
                section_node = nodes.section()
                title = env.titles[docname]
                section_node['ids'] = entry[0]['ids']
                title_node = nodes.title()
                ref_node = nodes.reference(classes=['feed-ref'])
                ref_node['internal'] = True
                ref_node['refdocname'] = docname
                ref_node['refuri'] = \
                        app.builder.get_relative_uri(fromdocname, docname)
                ref_node['refuri'] += '#' + section_node['ids'][0]
                ref_node += title[0]
                title_node += ref_node
                section_node += title_node
                for subnode in entry[0]:
                    if isinstance(subnode, (nodes.title, disqus)):
                        continue
                    if isinstance(subnode, entrycut):
                        para_node = nodes.paragraph()
                        ref_node = nodes.reference(classes=['feed-more'])
                        ref_node['internal'] = True
                        ref_node['refdocname'] = docname
                        ref_node['refuri'] = \
                                app.builder.get_relative_uri(fromdocname, docname)
                        ref_node['refuri'] += '#' + section_node['ids'][0]
                        ref_node += nodes.Text(u'Read more\u2026')
                        para_node += ref_node
                        section_node += para_node
                        break
                    section_node += subnode.deepcopy()
                env.resolve_references(section_node, fromdocname, app.builder)
                replacement.append(section_node)
                if rss_output:
                    rss_item_title = title[0]
                    rss_item_link = rss_link+app.builder.get_target_uri(docname)
                    rss_item_description = nodes.compound()
                    for subnode in entry[0]:
                        if isinstance(subnode, (nodes.title, entrymeta, disqus)):
                            continue
                        if isinstance(subnode, entrycut):
                            break
                        rss_item_description += subnode.deepcopy()
                    env.resolve_references(rss_item_description, docname,
                                           app.builder)
                    rss_item_description = app.builder.render_partial(
                                                    rss_item_description)['body']
                    rss_item_date = meta['date']
                    rss_item = PyRSS2Gen.RSSItem(
                            title = rss_item_title,
                            link = rss_item_link,
                            description = rss_item_description,
                            guid = PyRSS2Gen.Guid(rss_item_link),
                            pubDate = rss_item_date)
                    rss_items.append(rss_item)
        node.replace_self(replacement)
        if rss_output:
            rss_path = os.path.join(app.builder.outdir, rss_output)
            rss = PyRSS2Gen.RSS2(
                    title = rss_title,
                    link = rss_link,
                    description = rss_description,
                    lastBuildDate = datetime.datetime.utcnow(),
                    items = rss_items)
            rss.write_xml(open(rss_path, "w"), encoding="utf-8")


def setup(app):
    app.add_config_value('disqus_shortname', None, 'env')
    app.add_config_value('disqus_developer', False, 'env')
    app.add_directive('feed', FeedDirective)
    app.add_directive('feed-entry', FeedEntryDirective)
    app.add_directive('cut', CutDirective)
    app.add_directive('disqus', DisqusDirective)
    app.add_node(feed)
    app.add_node(entrymeta,
                 html=(visit_entrymeta, depart_entrymeta))
    app.add_node(entrycut,
                 html=(visit_entrycut, None))
    app.add_node(disqus,
                 html=(visit_disqus, None))
    app.connect('doctree-resolved', process_feed)


