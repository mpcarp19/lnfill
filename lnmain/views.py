from django.views.generic import ListView, DetailView
from django.template import loader
from django.forms import ModelForm
from django.http import HttpResponse

from lnmain.models import LNFillConf
from lnmain.forms import LNFillConfForm

# Create your views here.

def display_modelform(request,pk):

    # we grap the object associated with the passed pk
    try:
       p =  LNFillConf.objects.get(pk=pk)
       serial_id = p.serial_id
       t7info = serial_id.split(',')
    except:
       assert False

    # A HTTP POST?
    if request.method == 'POST':
        form = LNFillConfForm(request.POST, instance=p)
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
        print("I am here getting.")
        form = LNFillConfForm(instance=p)
        template = loader.get_template('lnmain/displaymodelform.html')
        context = {
            't7info': t7info,
            'form': form,
        }
        return HttpResponse(template.render(context,request))

def display_manifold(request):

    # let's pretend we found some LnControllers
    #t7_found_list = ['470010276', '470010916']
    t7_found_list = ['470010276']
    ch_Config_list = []

    # now let's grap informaton stored in the database
    for t7 in t7_found_list:
        serialID = t7+',1'
        try:
            # try first channel to see if it is in db table
            p = LNFillConf.objects.get(serial_id=serialID)
            d = {'serial': t7, 'chan': '1', 'type':chType[p.ch_type],
                 'name':p.ch_name , 'enable':enable[p.ch_enable] }
            ch_Config_list.append(d)
            
            # grap the rest of the channels
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

    template = loader.get_template('lnmain/displaymanifold.html')

    context = {
        't7_found_list': t7_found_list,
        'ch_Config_list': ch_Config_list,
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

class LNFillConfDetailView(DetailView):

    model = LNFillConf
    template_name_suffix = "_detail"

