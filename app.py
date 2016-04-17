from flask import Flask, Markup, render_template, \
    abort, send_from_directory
import markdown
import os.path

app = Flask(
    __name__,
    template_folder='resources/templates',
    static_folder='resources/public'
)

app.config['PAGE_DIR'] = 'resources/pages'

# TODO: move this into JSON maybe
navigation = [
    {
        'name': 'about',
        'title': 'About',
        'icon': 'info',
        'href': '/about'
    },
    {
        'name': 'projects',
        'title': 'Projects',
        'icon': 'code',
        'href': '/projects'
    },
    {
        'name': 'github',
        'title': 'GitHub',
        'icon': 'github',
        'href': 'https://github.com/axocomm',
        'target': 'blank'
    },
    {
        'name': 'bitbucket',
        'title': 'BitBucket',
        'icon': 'bitbucket',
        'href': 'https://bitbucket.org/axocomm',
        'target': 'blank'
    },
    {
        'name': 'linkedin',
        'title': 'LinkedIn',
        'icon': 'linkedin',
        'href': 'https://www.linkedin.com/axocomm',
        'target': 'blank'
    }
]

def get_navigation(base=None):
    """Get navigation items and add `active` class
    to current page.
    """
    if not base:
        return navigation

    return [
        dict(item, **{'active': item['name'] == base})
        for item in navigation
    ]

@app.route('/')
def render_home():
    return render_template(
        'home.html',
        navigation=get_navigation()
    )

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'resources/public'),
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
        content = Markup(markdown.markdown(file_content))
        base = page.split('/')[0]
        return render_template(
            'page.html',
            content=content,
            navigation=get_navigation(base)
        )

@app.errorhandler(404)
def render_404(error):
    return render_template(
        'error.html',
        error=error,
        navigation=get_navigation()
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
