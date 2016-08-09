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

## Feedback
DjangoLG is maintained by [Workonline Communications (Pty) Ltd](https://github.com/wolcomm).

Get in touch with us at communications@workonline.co.za or send a pull request.

## License
DjangoLG is released under the [Apache License version 2.0](http://www.apache.org/licenses/).

&copy; 2016 Workonline Communications (Pty) Ltd
