# coding: utf-8

import os

import markdown
import yaml
from flask import (
    Flask,
    Markup,
    render_template,
    abort,
    send_from_directory,
    request
)
from htmlmin.minify import html_minify

RESOURCE_DIR = os.path.join(os.getcwd(), 'resources')
PAGE_DIR = os.path.join(RESOURCE_DIR, 'pages')
ASSET_DIR = os.path.join(RESOURCE_DIR, 'public')
NAVIGATION = os.path.join(RESOURCE_DIR, 'navigation.yml')


class LambdaCodesApp(Flask):
    def __init__(self, import_name, **kwargs):
        super(LambdaCodesApp, self).__init__(import_name, **kwargs)
        self.site_title = 'λ.codes'

        self._nav_items = LambdaCodesApp._load_navigation(NAVIGATION)

    def render(self, template, **kwargs):
        """Render a template.

        This simply wraps Flask's render_template with a few extras:
          - Minifies content if not in debug mode
          - Includes navigation items with the base item marked active
        """
        html = render_template(
            template,
            **dict(kwargs, **self._page_options)
        )

        return html_minify(html) if not self.debug else html

    @property
    def page_dir(self):
        return self.config.get('PAGE_DIR')

    @property
    def _page_options(self):
        """Generate some extra options for template rendering.

        This includes marking the appropriate navigation item as
        active and passing the site_title to the template.
        """
        page_base = request.path.lstrip('/').split('/')[0]
        page_nav = [
            dict(item, **{'active': item['name'] == page_base})
            for item in self._nav_items
        ]

        return {'navigation': page_nav, 'site_title': self.site_title}

    @staticmethod
    def _load_navigation(filename):
        with open(filename) as fh:
            return yaml.load(fh.read())
        return []


app = LambdaCodesApp(
    __name__,
    template_folder=os.path.join(RESOURCE_DIR, 'templates'),
    static_folder=ASSET_DIR
)

app.config['PAGE_DIR'] = os.environ.get('PAGE_DIR', PAGE_DIR)


def find_title(content):
    """Try to find a page title using the first h1 in the Markdown
    source.
    """
    lines = content.split('\n')
    matches = [
        line for line in lines
        if line.startswith('# ')
    ]

    if not matches:
        return None
    else:
        return matches[0].lstrip('# ')


@app.route('/')
def render_home():
    return app.render('home.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(ASSET_DIR, 'favicon.png')


@app.route('/<path:page>')
def render_page(page):
    path = os.path.join(app.page_dir, page)

    if os.path.isdir(path):
        filename = os.path.join(path, 'index.md')
    else:
        filename = path + '.md'

    if not os.path.isfile(filename):
        abort(404)

    with open(filename) as fh:
        file_content = fh.read()
        title = find_title(file_content)
        content = Markup(markdown.markdown(
            file_content,
            extensions=['markdown.extensions.fenced_code']
        ))
        return app.render('page.html', content=content, title=title)


@app.errorhandler(404)
def render_404(_):
    return app.render(
        'error.html',
        error='That page does not seem to exist.'
    ), 404


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    debug = os.environ.get('DEBUG', False)
    app.run(debug=debug, host='0.0.0.0', port=port)
