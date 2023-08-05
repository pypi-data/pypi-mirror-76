=======
ColdCMS
=======

.. image:: coldcms/static/svg/coldcms.svg
    :width: 100
    :height: 100
    :alt: ColdCMS logo

.. image:: https://badge.fury.io/py/coldcms.svg

.. image:: https://readthedocs.org/projects/pip/badge/

.. image:: https://gitlab.com/hashbangfr/coldcms/badges/master/pipeline.svg

.. image:: https://gitlab.com/hashbangfr/coldcms/badges/master/coverage.svg


Goal
====

A fully functional CMS optimized for low consumption.

`Read blog posts <https://coldcms.hashbang.fr>`_ about this.


Benchmark
=========

`Benchmark details to Coldcms <https://gitlab.com/hashbangfr/coldcms/-/blob/master/benchmark/README.rst>`_


Description
===========
ColdCMS is a `Django <https://www.djangoproject.com>`_ project based on `Wagtail CMS <https://wagtail.io>`_ and `Bulma <https://bulma.io>`_
CSS framework.

The admin can edit websites through an intuitive and user-friendly interface. Different types of pages are pre-designed, making it possible
to have a nice-looking website without spending hours on it.

ColdCMS is especially designed for people who want to reduce the impact of their use of digital technologies on the environnement.

The client website consists of static pages, built with `Wagtail bakery <https://github.com/wagtail/wagtail-bakery>`_. The website pages
are generated and updated when necessary (e.g. when the admin publishes or modifies content).

Among other optimizations, the size of CSS files is reduced and unused CSS code is removed, using
`PurgeCSS <https://github.com/FullHuman/purgecss>`_ and `clean-css <https://github.com/jakubpawlowicz/clean-css-cli>`_.

ColdCMS supports Python >= 3.6.


How to use ColdCMS?
===================

You have access to a ColdCMS instance and you want to create a website
----------------------------------------------------------------------

You can find the user documentation here:

- `English documentation <https://coldcms.readthedocs.io/en/latest/>`_
- `Documentation en français <https://coldcms.readthedocs.io/fr/latest/>`_

You want to install ColdCMS
---------------------------

You have two options: docker installation or manual installation.

Docker installation
```````````````````

You will need docker-compose and docker with a running daemon.

We provide a sample ``docker/docker-compose.yml`` file. Feel free to modify it for your needs.

.. code-block:: shell

    cd docker && docker-compose up

Here are some env variables that you might want to change:

* ``POSTGRES_USER``, ``POSTGRES_PASSWORD``, ``POSTGRES_DB`` see
  `<https://github.com/docker-library/docs/blob/master/postgres/README.md#environment-variables>`_
* ``DB_URL``, the database connection URL, see `<https://github.com/jacobian/dj-database-url#url-schema>`_
* ``SECRET_KEY``, the `Django SECRET_KEY <https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY>`_,
  it should be a private, 40-character long randomly-generated string
* ``ALLOWED_HOSTS``, the coma-separated list of hosts allowed to serve your application, corresponds to the
  `Django ALLOWED_HOSTS <https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-ALLOWED_HOSTS>`_

You can then create an admin user which will have access to http://localhost/admin

.. code-block:: shell

    docker exec -it docker_backend_1 python3 manage.py createsuperuser

Manual installation
```````````````````

1. Choose a database
....................

We recommend using ``PostgreSQL``, but you can also use the default ``SQLite`` (no setup required). If you choose to use ``PostgreSQL``
take note of the host, port, database, user, and password you're using.

2. Install the backend part of ColdCMS
......................................

The backend is used to modify your website, it's located on ``https://your-site.tld/admin``

Download the latest release available here: https://gitlab.com/hashbangfr/coldcms/-/releases (or ``git clone`` the project, as you want)

Then you'll need to launch the ``wsgi`` application located here: https://gitlab.com/hashbangfr/coldcms/-/blob/master/coldcms/wsgi.py

You can do this using several projects:

- `uwsgi <http://uwsgi-docs.readthedocs.org/en/latest/>`_ (our preferred approach)
- `mod_wsgi (apache) <https://github.com/GrahamDumpleton/mod_wsgi>`_
- `CherryPy <https://github.com/cherrypy/cherrypy>`_
- ...

You'll have to pass some environment variables to the wsgi process (uwsgi for example), for the application to work as expected:

- ``DB_URL=postgres://coldcms:coldcms@db_host:5432/coldcms`` # adapt this for your setup, if you choose to use ``SQLite`` you can omit it
- ``BUILD_DIR=/srv/build`` # the directory under which the generated website will go,
  this directory will be served by your webserver (ex: nginx)
- ``STATIC_ROOT=/srv/build/static/`` # `Django STATIC_ROOT <https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-STATIC_ROOT>`_
  this directory needs to be served by your file server (ex: nginx) as well
- ``SECRET_KEY=CHANGE_ME`` # `Django SECRET_KEY <https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY>`_
  it should be a private, 40-character long randomly-generated string
- ``ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.tld``, the coma-separated list of hosts allowed to serve your application, corresponds to the
  `Django ALLOWED_HOSTS <https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-ALLOWED_HOSTS>`_

Here is a working example using ``uwsgi``, with the application located under ``/srv/app`` and using ``SQLite``:

.. code-block:: yaml

    [uwsgi]
    socket = 0.0.0.0:8000
    chdir = /srv/app/
    module = coldcms.wsgi:application
    master = true
    processes = 4
    threads = 2
    uid = coldcms
    gid = coldcms
    buffer-size = 65535
    env = BUILD_DIR=/srv/build
    env = STATIC_ROOT=/srv/build/static/
    env = SECRET_KEY=something_big_and_random


3. Setup Nginx to work with the backend
.......................................

Nginx acts like a file server which serves the static website generated by the backend. You can choose any kind of file server as long as
it can :

- serve files efficiently (HTML / images / assets ...)
- proxy requests to ``/admin`` to the actual ColdCMS backend (set up on the 2nd step)

An example of a functional nginx config is available here:
https://gitlab.com/hashbangfr/coldcms/-/blob/manual-install-doc/docker/nginx/nginx.conf

4 locations need to be served:

- ``/admin`` -> proxy to the python ColdCMS backend (step 2)
- ``/`` -> serve the HTML files generated by the backend (see ``BUILD_DIR`` in step 2)
- ``/media`` -> serve the medias files uploaded by the admin (it corresponds to ``$BUILD_DIR/media``)
- ``/static`` -> serve the static files (see ``STATIC_ROOT`` in step 2)

Feel free to adapt it for your needs

You are a developer and you want to quickly have a look
--------------------------------------------------------

**Note:** this has only been tested on Linux environments.

Install ColdCMS with pypi:

.. code-block:: shell

    pip install coldcms

Run the quick launch command:

.. code-block:: shell

    python -m coldcms

Before this command you can set the following environment variables :

- ``RUN_DJANGO_MIGRATION=0``: do not run the migrations

- ``SETUP_INITIAL_DATA=0``: do not setup the initial data, in case you want to keep the data you already have in your coldcms database

- ``COLLECT_STATIC=0``: do not collect the static files. Don't set that variable to 0 if it is your first time launching ColdCMS.

- ``CREATE_SUPERUSER=0``: do not create a new superuser (you can have several superuser at a time, but not with the same username or email)

- ``BUILD_ASSETS=0``: do not build build assets. Don't set that variable to 0 if it is your first time launching ColdCMS.

- ``BUILD_STATIC=0``: do not build static files. Don't set that variable to 0 if you've also set SETUP_INITIAL_DATA to 0.

Example: ``CREATE_SUPERUSER=0 python -m coldcms`` will run the migrations, setup some new initial data, but will not create a new superuser.

You are a developer and you want to contribute to ColdCMS
---------------------------------------------------------

Clone the gitlab repository, and read the **Dev** section below to install the ColdCMS development environment.

Follow the `contribution guidelines <https://gitlab.com/hashbangfr/coldcms/-/blob/master/CONTRIBUTING.rst>`_.

Dev
===

**Note:** this has only been tested on Linux environments.

1. Install the dependencies
---------------------------

Install ``libjpeg`` and ``zlib``, needed to work with images through the ``Pillow`` library.
If you have a debian-based distribution, use the following commands:

.. code-block:: shell

    sudo apt-get install zlib1g-dev
    sudo apt-get install libjpeg-dev

Also, please install PurgeCSS and clean-css, to reduce the size of CSS files:

.. code-block:: shell

    npm install -g purgecss@2.1.0 clean-css-cli@4.3.0

And to continue with javascript, please install static dependencies :

.. code-block:: shell

    (cd coldcms/static/ && npm i --save-dev)

We use sass to transpile sass files to CSS. Make sure that the binary `sass` from the `sassc` package is present in your $PATH.
In debian-based distributions, run the following:

.. code-block:: shell

    sudo apt-get install sassc
    sudo ln -s /usr/bin/sassc /usr/bin/sass # might be necessary if /usr/bin/sass doesn't exist after the previous command

Finally, run:

.. code-block:: shell

    pip install -r requirements_dev.txt


2. Create a database 
--------------------

By default, ``./manage.py migrate`` will create a sqlite3 database named ``coldcms``.

- If you want to use a different database engine, you can specify it in the environment variable ``DB_URL``. Make sure you have the
  proper database driver for the engine you want to use.
- If you want to use a different name for your sqlite database, you can specify it in the environment variable ``DB_NAME``
  (useless for some engines as it is directly specified in the url - see table below).

As advised in the `django documentation <https://docs.djangoproject.com/en/3.0/intro/tutorial02/#database-setup>`_, if you’re new to
databases, or you’re just interested in trying ColdCMS, use the default sqlite3 database, it is included in Python, so you won’t need to
install anything else to support your database. When starting your first real project, however, you may want to use a more scalable
database like PostgreSQL, to avoid database-switching headaches down the road.

+-------------+--------------------------------------------------+
| Engine      | DB_URL                                           |
+=============+==================================================+
| PostgreSQL  | ``postgres://USER:PASSWORD@HOST:PORT/NAME``      |
+-------------+--------------------------------------------------+
| PostGIS     | ``postgis://USER:PASSWORD@HOST:PORT/NAME``       |
+-------------+--------------------------------------------------+
| MSSQL       | ``mssql://USER:PASSWORD@HOST:PORT/NAME``         |
+-------------+--------------------------------------------------+
| MySQL       | ``mysql://USER:PASSWORD@HOST:PORT/NAME``         |
+-------------+--------------------------------------------------+
| MySQL (GIS) | ``mysqlgis://USER:PASSWORD@HOST:PORT/NAME``      |
+-------------+--------------------------------------------------+
| SQLite      | ``sqlite:///PATH``                               |
+-------------+--------------------------------------------------+
| SpatiaLite  | ``spatialite:///PATH``                           |
+-------------+--------------------------------------------------+
| Oracle      | ``oracle://USER:PASSWORD@HOST:PORT/NAME``        |
+-------------+--------------------------------------------------+
| Oracle (GIS)| ``oraclegis://USER:PASSWORD@HOST:PORT/NAME``     |
+-------------+--------------------------------------------------+
| Redshift    | ``redshift://USER:PASSWORD@HOST:PORT/NAME``      |
+-------------+--------------------------------------------------+

Replace PATH, USER, PASSWORD, HOST, PORT and NAME with the correct values.

`Source <https://github.com/jacobian/dj-database-url/blob/master/README.rst>`_

For example, if you want to use PostgreSQL :

.. code-block:: shell

    systemctl status postgresql # make sure postgresql is running
    createdb coldcms # create the coldcms postgres database
    sudo -u postgres psql
    CREATE USER username PASSWORD 'password';
    ALTER ROLE username WITH SUPERUSER;
    \q
    export DB_URL="postgres://username:password@localhost:5432/coldcms"
    

3. Launch the development server
--------------------------------

.. code-block:: shell  
    
    ./manage.py migrate
    ./manage.py collectstatic
    ./manage.py compilemessages
    ./manage.py createsuperuser
    ./manage.py setup_initial_data # optional - loads data of a basic home page
    ./manage.py runserver
