# lambda.codes

This is the source for [my website](https://lambda.codes) and is just
a simple Flask application that renders Markdown files.

## How it Works

### Page Rendering

Markdown files are placed inside `resources/pages/`. The
`/<path:page>` route will look inside this directory for either a file
with that name or, in the case of a subdirectory, an `index.md`
file. Flask's own Markup is then used to render the pages.

For example, visiting `/about/experience` would render the file at
`resources/pages/about/experience.md` and `/about` would render
`resources/pages/about/index.md`.

The homepage is a separate route that simply renders the
`resources/templates/home.html` template.

### Navigation

The navigation items are defined in `resources/navigation.yml`:

``` yaml
---
- href: /about
  icon: info
  name: about
  title: About
- href: /projects
  icon: code
  name: projects
  title: Projects
- href: https://github.com/axocomm
  icon: github
  name: github
  target: blank
  title: GitHub
- href: https://www.linkedin.com/in/tmaglione
  icon: linkedin
  name: linkedin
  target: blank
  title: LinkedIn
```

As is shown here, each item takes the following:

* `href`: just the navigation link
* `icon`: an icon to use (using [icons from Font
  Awesome](http://fontawesome.io/icons/))
* `name`: the name of the item (also used for determining which icon
  to highlight, for example `/about/experience` would highlight the
  `about` item)
* `title`: the title displayed
* `target` (optional): used for opening links in a new window

### Frontend Components

In `resources/src` you will find the following:

* `js`: for now, just `home-nav.js` used for handling the fading title
  effect of homepage icons
* `scss`: SCSS stylesheet sources

These are all compiled and placed in `resources/public` using Gulp.

## Running Locally

Running the app is quite simple:

* Create virtual environment and install Python requirements

    ```
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

* If you're using any of the Rake tasks, install Ruby requirements

    ```
    bundle
    ```

* Install Gulp globally (if not already installed) and Node
  requirements

    ```
    npm install -g gulp
    npm install
    ```

* Compile frontend resources

    ```
    gulp build
    ```

You may also start watching resources for automatic compilation with
`gulp d`.

* Run the server

    ```
    DEBUG=true python -m app
    ```

    The `DEBUG` environment variable being set will run the server in
    debug mode and disable HTML minification.

    You can also specify an alternate directory for pages by setting
    the `PAGE_DIR` environment variable before running the server.

At this point the application should be available at
`http://localhost:5000`.

## Testing

A few tests are included and are located in `test_app.py` which check
the following:

* homepage rendering
* Markdown file rendering
* `index.md` rendering
* missing page returning a 404
* HTML minification disabled when `DEBUG` is set

and can be run with `python test_app.py`.

## Deployment

The `lcdfile` in this repository now takes care of deployments (minus
Nginx configuration, which should be forthcoming). This file just
contains some lines of Ruby code that handle things like cloning the
repository, building the Docker image, and running the
container. Deployment is a matter of creating a simple configuration
file with some SSH information (like
`resources/site-config.json.example`) and running `lcd deploy`. If
you'd like you can have a look at the [lcdeploy
repository](https://github.com/axocomm/lcdeploy). Just keep in mind
the tool is extremely WIP (and being rewritten).

The steps run in this file, which can be run manually if desired, are
as follows:

1. Clone this repository

2. Build the Docker image specified in the `Dockerfile`

    `docker build -t lambda-codes:latest .`

3. Run the Docker container

    ```
    docker run \
      -d \
      --name lambda-codes \
      -p 5000:5000 \
      -v $(pwd)/resources/pages:/pages \
      lambda-codes:latest
    ```

### Nginx

Configuration for Nginx just involves setting up a reverse proxy. For
example:

``` nginx
server {
  listen 80;
  server_name lambda.codes;

  expires 31d;

  access_log /var/log/nginx/lambda.codes.access.log;
  error_log /var/log/nginx/lambda.codes.error.log info;

  location / {
    proxy_pass http://localhost:5000;
    proxy_set_header Host $http_host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_redirect off;
  }

  root /www/lambda.codes;
  index index.html;
}
```

## Managing Pages

Changes to page content can be pushed without doing another deploy
either by SCPing or using the `push_pages` Rake task, e.g.

```
ENVIRONMENT=prod rake push_pages
```

Likewise, any pages updated remotely can be pulled with `pull_pages`.
