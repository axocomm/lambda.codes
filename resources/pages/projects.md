# Selected Projects

### lambda.codes

[GitHub](https://github.com/axocomm/lambda.codes)<br>
This site is a simple Flask application that renders pages from
Markdown files.  It lives inside a Docker container running on Fedora
Server.

Styles are from scratch but do start with the
[CSS Reset](http://meyerweb.com/eric/tools/css/reset/). Navigation icons
come courtesy of [Font Awesome](https://fontawesome.com).

### lcdeploy

[GitHub](https://github.com/axocomm/lcdeploy)<br>
This is a Ruby gem that allows deployments to be specified using a
number of straightforward step helper functions (`create_directory`,
`copy_file`, `clone_repository`, etc.) and other Ruby code in an
[`lcdfile`](https://github.com/axocomm/lambda.codes/blob/master/lcdfile).
It tries to be a little more robust than using `Rakefile`s or shell
scripts without getting to the level of Chef or Ansible and
facilitates deploys of basic applications from individual project
directories using a single file. This is currently getting overhauled.

### rupervisor

[GitHub](https://github.com/axocomm/rupervisor)<br>
This is another Ruby gem that provides a DSL for defining simple
pipelines. These pipelines can involve more or less any command and
supports taking actions based on return code, dynamic population of
arguments, configurable retries, and more.

### nago

Nago is a system/service monitoring utility similar to Nagios. Through
the use of a small agent program, various checks (e.g. CPU load,
Docker containers running, etc.) can be enabled and run on registered
machines. Check results are saved (and preserved with configurable
retention time) to a Redis database for viewing on a dashboard.

### vagrant-wordpress

[GitHub](https://github.com/axocomm/vagrant-wordpress)<br>
A Vagrant setup that aims to provide quick and easy access to a LEMP
stack and ready-to-use WordPress installation for local development

### puff-puff-dash

[GitHub](https://github.com/axocomm/puff-puff-dash)<br>
A link management application mostly written to experiment with
ClojureScript and Reagent. Allows management and querying of links
(favorite music, videos, images, etc.) from various sources.
Currently wants local JSON, but eventually I hope to have it interact
directly with the APIs of SoundCloud, Reddit, YouTube, and more.

### wp-docker-dev

[GitHub](https://github.com/axocomm/wp-docker-dev)<br>
A simple Docker-based WordPress setup that provides an easy-to-use
environment for working on multiple local development installations

### racknews

[GitHub](https://github.com/axocomm/racknews2)<br>
A simple RackTables API and reporting tool

Most of these are perpetually WIP and others unfortunately private for
now. More to come soon (hopefully).
