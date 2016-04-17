from flask import Flask, Markup, render_template, abort
import markdown
import os.path

app = Flask(
    __name__,
    template_folder='resources/templates',
    static_folder='resources/public'
)

app.config['PAGE_DIR'] = 'resources/pages'

@app.route('/')
def index():
    return 'Foo'

@app.route('/<path:page>')
def render_page(page):
    page_dir = app.config['PAGE_DIR']
    filename = '%s.md' % os.path.join(page_dir, page)

    if not os.path.isfile(filename):
        abort(404)

    with open(filename) as fh:
        file_content = fh.read()
        content = Markup(markdown.markdown(file_content))
        return render_template('page.html', content=content)

@app.errorhandler(404)
def render_404(error):
    return render_template('error.html', error=error)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0'
    )
