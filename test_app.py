# coding: utf-8

import unittest

import app as xyzy


class XyzyAppTestCase(unittest.TestCase):
    def setUp(self):
        xyzy.app.testing = True
        xyzy.app.debug = True
        self.app = xyzy.app.test_client()

    def test_homepage_renders(self):
        """The app should render the homepage at '/'."""
        rv = self.app.get('/')

        assert rv.status == '200 OK'
        assert bytes('<h1 id="home-title">λ.codes</h1>', 'UTF-8') in rv.data

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
        """The app should return a 404 status and display an error if the page
        requested is not found.
        """
        rv = self.app.get('/nothing')
        assert rv.status == '404 NOT FOUND'
        assert b'<h1>Error</h1>' in rv.data
        assert b'That page does not seem to exist' in rv.data

    def test_minification_without_debug(self):
        """HTML Minification should occur if not in debug mode."""
        xyzy.app.debug = False
        rv = self.app.get('/')
        assert rv.status == '200 OK'
        assert b'<!DOCTYPE html><html><head><meta charset="utf-8"/>' in rv.data

    def test_minification_with_debug(self):
        """HTML minification should not occur if in debug mode."""
        xyzy.app.debug = True
        rv = self.app.get('/')
        assert rv.status == '200 OK'
        assert b'<!doctype html>\n<html>\n  <head>' in rv.data


if __name__ == '__main__':
    unittest.main()
