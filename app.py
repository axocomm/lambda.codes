import os
import os.path

import markdown
import yaml
from flask import (
    Flask,
    Markup,
    render_template,
    abort,
    send_from_directory
)
from htmlmin.minify import html_minify

RESOURCE_DIR = 'resources'
PAGE_DIR = os.path.join(RESOURCE_DIR, 'pages')
NAVIGATION = os.path.join(RESOURCE_DIR, 'navigation.yml')

app = Flask(
    __name__,
    template_folder=os.path.join(RESOURCE_DIR, 'templates'),
    static_folder=os.path.join(RESOURCE_DIR, 'public')
)
app.config['PAGE_DIR'] = os.environ.get('PAGE_DIR', PAGE_DIR)


def load_navigation(filename):
    with open(filename) as fh:
        return yaml.load(fh.read())
    return []


def get_navigation(base=None):
    """Get navigation items and add `active` class
    to current page.
    """
    navigation = load_navigation(NAVIGATION)
    if not base:
        return navigation

    return [
        dict(item, **{'active': item['name'] == base})
        for item in navigation
    ]


def find_title(content):
    """Try to find a page title using the first h1 in the Markdown
    source.
    """
    lines = content.split('\n')
    matches = [
        line for line in lines
        if line.startswith('#')
    ]

    if not matches:
        return None
    else:
        return matches[0].lstrip('# ')


def render_content(content):
    """Render the given content, minified unless `app.debug` is set."""
    return html_minify(content) if not app.debug else content


@app.route('/')
def render_home():
    rendered = render_template(
        'home.html',
        navigation=get_navigation()
    )

    return render_content(rendered)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, RESOURCE_DIR, 'public'),
        'favicon.png'
    )


@app.route('/<path:page>')
def render_page(page):
    page_dir = app.config['PAGE_DIR']
    path = os.path.join(page_dir, page)

    if os.path.isdir(path):
        filename = os.path.join(path, 'index.md')
    else:
        filename = path + '.md'

    if not os.path.isfile(filename):
        abort(404)

    with open(filename) as fh:
        file_content = fh.read()
        title = find_title(file_content)
        content = Markup(markdown.markdown(file_content))
        base = page.split('/')[0]
        rendered = render_template(
            'page.html',
            content=content,
            navigation=get_navigation(base),
            title=title
        )

        return render_content(rendered)


@app.errorhandler(404)
def render_404(error):
    return render_template(
        'error.html',
        error=error,
        navigation=get_navigation()
    ), 404


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    debug = os.environ.get('DEBUG', False)
    app.run(debug=debug, host='0.0.0.0', port=port)
