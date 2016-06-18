from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.forms import formset_factory
from django.forms import ModelForm
from lnmain.models import *
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from lnmain.forms import ConfigForm, LNFillConfForm

import datetime

# Create your views here.

enable = ['disabled','enabled']
chType = ['manifold','vent','detector']


def index(request):
    # let's pretend we found some LnControllers
    t7_found_list = ['470010276', '470010916']
    ch_Config_list = []
    # now let's grap informaton stored in the database

    for t7 in t7_found_list:
        serialID = t7+',1'
        try:
            p = LNFillConf.objects.get(serial_id=serialID)
            d = {'serial': t7, 'chan': '1', 'type':chType[p.ch_type],
                 'name':p.ch_name , 'enable':enable[p.ch_enable] }
            ch_Config_list.append(d)
            
            for chan in range(2,13):
                serialID = t7 + ','+ str(chan)
                p = LNFillConf.objects.get(serial_id=serialID)
                d = {'serial': t7, 'chan': str(chan), 'type':chType[p.ch_type],
                     'name':p.ch_name , 'enable':enable[p.ch_enable] }
                ch_Config_list.append(d) 
                       
        except:        
            d = {'serial': t7, 'chan': '0', 'type': 'Dead', 'name':'xxxx', 
                 'enable':'unknown' }
            ch_Config_list.append(d)
            #assert False                  # triggers error page

    template = loader.get_template('lnmain/index.html')
    context = {
        't7_found_list': t7_found_list,
        'ch_Config_list': ch_Config_list,
    }

    return HttpResponse(template.render(context,request))

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def display_form(request):
    # let's pretend we found some LnControllers
    t7_found = '470010276'
    ch_Config_list = []

    # now let's grap informaton stored in the database
    if request.method == 'POST':
        ConfigFormSet = formset_factory(ConfigForm)
        formset  = ConfigFormSet(request.POST)
    else:
        serialID = t7_found+',1'
        try:
            p = LNFillConf.objects.get(serial_id=serialID)
            d = {'chan': '1', 'ctype':chType[p.ch_type],
                 'cname':p.ch_name , 'cenable':enable[p.ch_enable] }
            ch_Config_list.append(d)
            
            for chan in range(2,13):
                serialID = t7_found + ','+ str(chan)
                p = LNFillConf.objects.get(serial_id=serialID)
                d = {'chan': str(chan), 'ctype':chType[p.ch_type],
                     'cname':p.ch_name , 'cenable':enable[p.ch_enable] }
                ch_Config_list.append(d) 
                       
        except:        
            d = {'chan': '0', 'ctype': 'Dead', 'cname':'xxxx', 
                 'cenable':'unknown' }
            ch_Config_list.append(d)
        
    #assert False                  # triggers error page

    # ch_Config_list now contains the values of our form - we now need to populate our formset
 
        ConfigFormSet = formset_factory(ConfigForm)
        formset  = ConfigFormSet( initial=[ {'chan':d.get('chan'), 'ctype':d.get('ctype'), 'cname':d.get('cname'),
                                              'cenable':d.get('cenable')} for d in ch_Config_list ])

        template = loader.get_template('lnmain/displayform.html')
        context = {
            't7_found': t7_found,
            'formset': formset,
        }

        return HttpResponse(template.render(context,request))

def display_modelform(request):
    # let's pretend we found some LnControllers
    t7_found = '470010276'
    serialID = t7_found+',1'


    # A HTTP POST?
    if request.method == 'POST':
        p = LNFillConf.objects.get(serial_id=serialID)
        form = LNFillConfForm(request.POST, instance=p)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save()
            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
    else:

        try:
            p = LNFillConf.objects.get(serial_id=serialID)
        except:
            assert False

        form = LNFillConfForm(instance=p)
        template = loader.get_template('lnmain/displaymodelform.html')
        context = {
            't7_found': t7_found,
            'form': form,
        }
        return HttpResponse(template.render(context,request))

class LNFillConfList(ListView):

    model = LNFillConf
    template_name = 'lnfillconf_list.html'
    t7_found = ['470010276', '470010916']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LNFillConfList, self).get_context_data(**kwargs)
        # Add in the T7's you know about.
        context['t7_found'] = self.t7_found
        # add in the objects of interest from a query of the table. 
        #context['lnfill_list'] = LNFillConf.objects.filter(serial_id__startswith=self.t7_found)
        context['lnfill_list'] = LNFillConf.objects.all()
        #print "I am here!"
        return context

    def dispatch(self, request, *args, **kwargs):
        print(request,args,kwargs)
        return super(LNFillConfList, self).dispatch(request, *args, **kwargs)

class LNMainActionMixin(object):

     @property
     def action(self):
         msg = "{0} is missing action.".format(self.__class__)
         raise NotImplementedError(msg)

     def form_valid(self, form):
         msg = "Flavor {0}!".format(self.action)
         messages.info(self.request, msg)
         return super(FlavorActionMixin, self).form_valid(form)

class LNFillConfCreateView(CreateView):
  
    model = LNFillConf
    fields = '__all__'
    action = 'created'
    def dispatch(self, request, *args, **kwargs):
        print(request,args,kwargs)
        print(request.method)
        return super(LNFillConfCreateView, self).dispatch(request, *args, **kwargs)

class LNFillConfUpdateView(UpdateView):

    model = LNFillConf
    fields = ['serial_id', 'ch_type', 'ch_name', 'ch_enable']
    action = 'updated'
    success_url = 'lnmain'

    def dispatch(self, request, *args, **kwargs):
        print(request,args,kwargs)
        print(request.method)
        return super(LNFillConfUpdateView, self).dispatch(request, *args, **kwargs)


class LNFillConfView(DetailView):

    model = LNFillConf


