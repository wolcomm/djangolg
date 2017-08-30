[![PyPI](https://img.shields.io/pypi/v/djangolg.svg)](https://pypi.python.org/pypi/djangolg)
[![PyPI](https://img.shields.io/pypi/dm/djangolg.svg)](https://pypi.python.org/pypi/djangolg)
[![Build Status](https://travis-ci.org/wolcomm/djangolg.svg?branch=master)](https://travis-ci.org/wolcomm/djangolg)
[![codecov](https://codecov.io/gh/wolcomm/djangolg/branch/master/graph/badge.svg)](https://codecov.io/gh/wolcomm/djangolg)

# DjangoLG
A BGP looking glass based on the Django web framework

## Features
* User interface
    * Polished web UI based on jQuery and Bootstrap
    * Ajax/JSON query processing
    * Customisable Django templates
* Multi-vendor device support using Napalm drivers
* Supported query types
    * BGP paths/bestpath/longer paths by prefix
    * BGP paths by AS_PATH regexp
    * ICMP Ping
    * Traceroute
    * Framework for adding new query types easily
* Supported NOS command dialects
    * Cisco IOS-XE/Classic
    * "Dialect" framework for defining new syntax mappings
* Security
    * SSH2-only command execution
    * Multi-layered parameter verification
    * Session and command authorisation framework:
        * Google reCaptcha support
        * Source IP address enforcement per session
        * Max queries enforcement per session
        * Max time enforcement per session

## Quick Start
To install in a virtualenv called `$VENV`:

1.  Create and activate the vitrualenv:
    ```
    virtualenv $VENV
    cd $VENV
    source bin/activate
    ```

2.  Install Django and DjangoLG using `pip`:
    ```
    pip install Django
    pip install djangolg
    ```

3.  Create a Django project:
    ```
    django-admin startproject demo_lg
    cd demo_lg
    ```

4.  Edit your project's settings file (e.g. `vi demo_lg/settings.py`):
    * Add `djangolg.apps.DjangolgConfig` to `INSTALLED_APPS`.
    * Add `DJANGOLG_` settings as required.

5.  Edit your project's urls file (e.g. `vi demo_lg/urls.py`):
    * Add the `include` function to the module's imports:
      ```diff
      -from django.conf.urls import url
      +from django.conf.urls import url, include
      ```
    * Add an entry to `urlpatterns`:
      ```diff
      urlpatterns = [
      +   url(r'^lg/', include('djangolg.urls')),
          url(r'^admin/', admin.site.urls),
      ]
      ```

6.  Create your database tables using `manage.py`:
    ```
    ./manage.py migrate
    ```

7.  Create a set of SSH credentials, a location and some routers:
    ```
    ./manage.py lg add credentials --name default_credentials --type 0 --username test_user --password test_password
    ./manage.py lg add locations --name Some Place --sitecode ABC-123
    ./manage.py lg add routers --hostname router1.example.net --dialect ios --credentials 1 --location 1
    ./manage.py lg add routers --hostname router2.example.net --dialect ios --credentials 1 --location 1
    ```

8.  Run the development server:
    ```
    ./manage.py runserver [::]:8000
    ```

9.  Open a browser, navigate to `localhost:8000`, and check that everything is working.

## Feedback
DjangoLG is maintained by [Workonline Communications (Pty) Ltd](https://github.com/wolcomm).

Get in touch with us at communications@workonline.co.za or [raise an issue](https://github.com/wolcomm/djangolg/issues/new).

## License
DjangoLG is released under the [Apache License version 2.0](http://www.apache.org/licenses/).

&copy; 2016-2017 Workonline Communications (Pty) Ltd
