"""
We render a web page with only one file if we include the right stuff
"""
import os
import sys
from django.conf import settings


DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32)) 
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOST=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ), 
)

from django.conf.urls import url 
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
# This is the view
def index(request):
    greeting = 'Hey Buddy!'
    return HttpResponse(greeting)
# This is the URL pattern
urlpatterns = (
        url(r'^$', index),
)

# specific to wsgi server
application = get_wsgi_application()

if __name__ == "__main__":

    # run this using the command $python hellow_world.py runserver
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
