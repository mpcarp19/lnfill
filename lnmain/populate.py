#!/usr/bin/env python
# Setup the Django environment so we can access our models
import os, sys
import datetime

proj_path = '/webapps/lnfill_django/lnfill'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lnfill.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# needs to go here
from lnmain.models import *

def main():

# This method will do the main processing

    if len(sys.argv) < 2:
        print "command: LNFill.py configfile"
        return

# open and process the config file

    #configfile = "T7-470010276.config"
    configfile = str(sys.argv[1])
    print configfile

    try:
       config = open(configfile,"r")
    except Exception as e:  # figure out what exception 
       print "Could not find configuration file - Please check file name."
       return

    content = config.readlines() 

    # parse content
    for line in content:
       if line.startswith("#Serial"):
           serialnum = line.split("=")[1].strip()
           print "Serial Number is ",serialnum
       elif line.startswith("#Config"):
           configure=1
       elif line.startswith("#"):
           ncommet=0
       elif configure==1:
           results = line.split(",")
           if len(results) == 4:
               i = 0
               for result in results:  
                   results[i] = result.strip()
                   i=i+1
               # now update the database
               chan = int(results[0])
               results[0] = serialnum + ','+ str(chan)
               print 'updating -- ',results[0], results[1], results[2], results[3]
               c = Ch_Addresses.objects.get(id=chan)
               p, created = LNFillConf.objects.get_or_create(serial_id=results[0],ch_addresses=c)
               p.ch_type = int(results[1])
               p.ch_name = results[2]
               p.ch_enable = results[3]
               p.save()

    return               
# Now run main
main()

