from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder='resources/templates',
    static_folder='resources/public'
)

@app.route('/')
def index():
    return 'Foo'

@app.route('/<path:page>')
def render_page(page):
    return render_template('page.html', page=page)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0'
    )
