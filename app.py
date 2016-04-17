from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Foo'

@app.route('/<path:page>')
def render_page(page):
    return 'The page is %s ' % page

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0'
    )
