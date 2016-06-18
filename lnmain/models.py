from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from django.db import models

# Create your models here.
'''
This data base maps the LN-Fill module inputs to registers on the T7.
We need to create 12 and only 12 items in order and allow the auto generated id
to represent the channel. 
'''
class Ch_Addresses(models.Model):
    #channel_id = models.IntegerField()
    pt100_address      = models.CharField(max_length=6)  
    overflow_address   = models.CharField(max_length=6)
    valve_address      = models.CharField(max_length=6)

    def __unicode__(self):
        return "Channel %d" % (self.id)
'''
This database will contain the current configuration of one or more T7 Modules.
A one to many relationship exists between LNConfig and Channel_Adressess
Choices are used for channel_type and channel_enable fields. The serial number and channel
are combined into a CommaSeparatedIntgerField allowing us to declare this entry unique.
'''
class LNFillConf(models.Model):

    CH_TYPE_CHOICES = (
        (0, 'Manifold'),
        (1, 'Vent'),
        (2, 'Detector'),
    )
    ENABLE_CHOICES = (
        (0, 'Disable'),
        (1, 'Enable'),
    )

    serial_id = models.CommaSeparatedIntegerField(max_length=20,unique=True)
    #channel_id = models.IntegerField()
    ch_type = models.IntegerField(default=2,choices=CH_TYPE_CHOICES)
    ch_name = models.CharField(max_length=30,blank=True)
    ch_enable = models.IntegerField(default=0,choices=ENABLE_CHOICES)
    ch_addresses = models.ForeignKey(Ch_Addresses,on_delete=models.CASCADE,blank=True,default=1)
    
    def __unicode__(self):
        serialID = self.serial_id
        l = serialID.split(',')
        if len(l) == 2:
          return "Serial Number %s : Channel %s" % (l[0], l[1])
        else:
          return "Serial ID is not defined ???"

    def get_absolute_url(self):
        return reverse('detail_view', kwargs={'pk': self.pk})
  
