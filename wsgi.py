#!/usr/bin/env python
import os

from flask_test import app as application
from flask_test import main

#
# Below for testing only
#
if __name__ == '__main__':
    main()
    """
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    # Wait for a single request, serve it and quit.
    httpd.serve_forever()
    """
