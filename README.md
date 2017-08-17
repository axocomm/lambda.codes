# xyzyxyzy.xyz

This is the source for [my website](https://xyzyxyzy.xyz) and is just a simple Flask application that renders Markdown files.

## How it Works

### Page Rendering

Markdown files are placed inside `resources/pages/`. The `/<path:page>` route will look inside this directory for either a file with that name or, in the case of a subdirectory, an `index.md` file. Flask's own Markup is then used to render the pages.

For example, visiting `/about/experience` would render the file at `resources/pages/about/experience.md` and `/about` would render `resources/pages/about/index.md`.

The homepage is a separate route that simply renders the `resources/templates/home.html` template.

### Navigation

The navigation items are defined in `resources/navigation.yml`:

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

As is shown here, each item takes the following:

* `href`: just the navigation link
* `icon`: an icon to use (using [icons from Font Awesome](http://fontawesome.io/icons/))
* `name`: the name of the item (used for determining which navigation item to highlight)
* `title`: the title displayed
* `target` (optional): used for opening links in a new window

### Frontend Components

In `resources/src` you will find the following:

* `js`: for now, just `home-nav.js` used for handling the fading title effect of homepage icons
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
    
* Install Gulp globally (if not already installed) and Node requirements

    ```
    npm install -g gulp
    npm install
    ```

* Compile frontend resources

    ```
    gulp build
    ```
	
	You may also start watching resources for automatic compilation with `gulp d`.

* Run the server

    ```
    python -m app
    ```
    
    You can specify an alternate directory for pages by setting the `PAGE_DIR` environment variable before running the server.
	
At this point the application should be available at `http://localhost:5000`.

## Testing

A few tests are included and are located in `test_app.py` which check the following:

* homepage rendering
* Markdown file rendering
* `index.md` rendering
* missing page returning a 404

and can be run with `python test_app.py`.

## Deployment

The deploy process is probably not ideal at the moment but is still pretty straightforward (I think). The process is as follows:

1. Builds frontend resources
2. Copies required files to the remote server
    * application source
    * Rakefile
    * resources
    * pages
3. Installs Ruby requirements
4. Builds Docker container
5. Stops and removes existing container if applicable
6. Starts the new container

The `deploy` Rake task takes care of this, e.g.

    ENVIRONMENT=prod rake deploy

### Configuration

Deployment configuration is done per-environment in `resources/config.yml` and should look as follows:

    ---
    deploy:
      prod:
        host: xyzyxyzy.xyz
        user: deploy
        ssh_port: 2200
        remote_path: "/home/deploy/xyzy-min"
        page_dir: "/home/deploy/xyzy-min/resources/pages"
        listen_port: 5000
        name: xyzy-min

Most of these are pretty self-explanatory. `name` just specifies the name of the Docker container. The `listen_port` defines which port should be exposed.

A few environment variables also come into play:

* `PORT` (defaults to 5000): determines which port Flask itself should be listening on
* `ENVIRONMENT` (defaults to 'staging'): which deployment configuration to use

### Nginx

Configuration for Nginx just involves setting up a reverse proxy. For example:

    server {
      listen 80;
      server_name xyzyxyzy.xyz;

      expires 31d;

      access_log /var/log/nginx/xyzyxyzy.xyz.access.log;
      error_log /var/log/nginx/xyzyxyzy.xyz.error.log info;

      location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $http_host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
      }

      root /www/xyzyxyzy.xyz;
      index index.html;
    }
    
### Managing Pages

Changes to page content can be pushed without doing another deploy either by SCPing or using the `push_pages` Rake task, e.g.

    ENVIRONMENT=prod rake push_pages
    
Likewise, any pages updated remotely can be pulled with `pull_pages`.