import unittest

import app as xyzy


class XyzyAppTestCase(unittest.TestCase):
    def setUp(self):
        xyzy.app.testing = True
        self.app = xyzy.app.test_client()

    def test_homepage_renders(self):
        rv = self.app.get('/')

        assert rv.status == '200 OK'
        assert b'<h1 id="home-title">xyzy</h1>' in rv.data

    def test_page_renders_from_file(self):
        """The app should be able to render a Markdown file."""
        rv = self.app.get('/projects')

        assert rv.status == '200 OK'
        assert b'<h1>Selected Projects</h1>' in rv.data

    def test_page_renders_index_file(self):
        """The app should be able to render an `index.md` if the path points
        to a directory.
        """
        rv = self.app.get('/about')

        assert rv.status == '200 OK'
        assert b'<h1>About</h1>' in rv.data

    def test_missing_page_returns_404(self):
        rv = self.app.get('/nothing')
        assert rv.status == '404 NOT FOUND'


if __name__ == '__main__':
    unittest.main()
