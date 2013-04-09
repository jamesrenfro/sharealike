activate_this = "/home/ubuntu/poochable/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

import os
import sys

path = '/home/ubuntu/poochable'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'poochable.settings'

# activate virtualenv

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
import djcelery
djcelery.setup_loader()
