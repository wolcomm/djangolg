[![PyPI](https://img.shields.io/pypi/v/djangolg.svg)](https://pypi.python.org/pypi/djangolg)
[![Build Status](https://travis-ci.org/wolcomm/djangolg.svg?branch=master)](https://travis-ci.org/wolcomm/djangolg)

# DjangoLG
A BGP looking glass based on the Django web framework

## Features
* User interface
    * Polished web UI based on jQuery and Bootstrap
    * Ajax/JSON query processing
    * Customisable Django templates
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
    * Pubkey authentication (coming soon)
    * Multi-layered parameter verification
    * Session and command authorisation framework:
        * Google reCaptcha support
        * Source IP address enforcement per session
        * Max queries enforcement per session
        * Max time enforcement per session

## Quick Start
1. Install from PyPI (possibly in a virtenv):
   ```
   pip install djangolg
   ```

2. Add `djangolg.apps.DjangolgConfig` to your project `INSTALLED_APPS`.
3. Add an include (e.g. `url(r'^', include('djangolg.urls')),`) to your project `urlpatterns`.
4. Copy example settings in the `djangolg` package directory and edit the defaults:
   ```
   cp local_settings.py.example local_settings.py
   vi local_settings.py
   ```

5. Create your database tables using `manage.py`:
   ```
   python manage.py makemigrations djangolg
   python manage.py migrate
   ```
   
6. Create a set of SSH credentials, a location and some routers:
   ```
   python manage.py lg add credentials --name default_credentials --type 0 --username test_user --password test_password
   python manage.py lg add locations --name Some Place --sitecode ABC-123
   python manage.py lg add routers --hostname router1.example.net --dialect cisco_ios-xe --credentials 1 --location 1
   python manage.py lg add routers --hostname router2.example.net --dialect cisco_ios-xe --credentials 1 --location 1
   ```

7. Run the development server, open a browser, and check that everything is working:
   ```
   python manage.py runserver
   ```


## Feedback
DjangoLG is maintained by [Workonline Communications (Pty) Ltd](https://github.com/wolcomm).

Get in touch with us at communications@workonline.co.za or [raise an issue](https://github.com/wolcomm/djangolg/issues/new).

## License
DjangoLG is released under the [Apache License version 2.0](http://www.apache.org/licenses/).

&copy; 2016 Workonline Communications (Pty) Ltd
