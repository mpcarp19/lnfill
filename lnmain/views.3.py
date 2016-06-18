from lnmain.models import *
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from lnmain.forms import LNFillConfForm
from django.template import loader
from django.forms import ModelForm
from django.http import HttpResponse

import datetime

# Create your views here.

def display_modelform(request,pk):
    # we grap the object associated with the passed pk

    # A HTTP POST?
    if request.method == 'POST':
        #p = LNFillConf.objects.get(serial_id=serialID)
        p =  LNFillConf.objects.get(pk=pk)
        form = LNFillConfForm(request.POST, instance=p)
        print("I am here Posting.")
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save()
            # Now call the index() view.
            # The user will be shown the homepage.
            # return index(request)
            request.method = 'GET'  # seems to be the trick change from POST to GET
            return LNFillConfList.as_view()(request)
    else:
        try:
            #p = LNFillConf.objects.get(serial_id=serialID)
            p = LNFillConf.objects.get(pk=pk)
            serial_id = p.serial_id
            t7info = serial_id.split(',')
        except:
            assert False

        print("I am here getting.")
        form = LNFillConfForm(instance=p)
        template = loader.get_template('lnmain/displaymodelform.html')
        context = {
            't7info': t7info,
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
        context['lnfill_list'] = LNFillConf.objects.all().order_by('pk')
        #print "I am here!"
        return context

    def dispatch(self, request, *args, **kwargs):
        print(request,args,kwargs)
        print(request.method)
        return super(LNFillConfList, self).dispatch(request, *args, **kwargs)

class LNFillConfCreateView(CreateView):
  
    model = LNFillConf
    fields = '__all__'
    #action = 'created'
    def dispatch(self, request, *args, **kwargs):
        print(request,args,kwargs)
        print(request.method)
        return super(LNFillConfCreateView, self).dispatch(request, *args, **kwargs)

class LNFillConfUpdateView(UpdateView):

    model = LNFillConf
#    fields = ['serial_id', 'ch_type', 'ch_name', 'ch_enable']
    fields = '__all__'
    #action = 'updated'
    #success_url = 'lnmain'

    def dispatch(self, request, *args, **kwargs):
        print(request,args,kwargs)
        print(request.method)
        #if str(request).find("csrf") != -1: 
          #request.method = "POST"
          #print request.method
        #assert False
        return super(LNFillConfUpdateView, self).dispatch(request, *args, **kwargs)


class LNFillConfDetailView(DetailView):

    model = LNFillConf
    template_name_suffix = "_detail"

