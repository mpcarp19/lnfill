from django.conf.urls import url
from . import views
#from lnmain.views import LNFillConfList, LNFillConfUpdateView, LNFillConfCreateView, LNFillConfDetailView
from lnmain.views import LNFillConfList, LNFillConfDetailView

urlpatterns = [
    # ex: /lnmain/
    #url(r'^$', views.index, name='index'),
    url(r'^$',LNFillConfList.as_view(),name='index'),
    url(r'^index/$',LNFillConfList.as_view(),name='index'),
#    url(r'^time/$',views.current_datetime, name='current_datetime'),
#    url(r'^info/$',views.display_meta, name='display_meta'),
#    url(r'^form/$',views.display_form, name='display_form'),
    url(r'^modelform/(?P<pk>\d+)/$',views.display_modelform, name='display_modelform'),
    url(r'^manifold/$',views.display_manifold,name='display_manifold'),
#    url(r'^createform/$',LNFillConfCreateView.as_view(), name='create_form'),
#    url(r'^(?P<pk>\d+)/updateform/$',LNFillConfUpdateView.as_view(), name='update_form'),
    url(r'^detailview/(?P<pk>\d+)/$',LNFillConfDetailView.as_view(), name='detail_view'),
]

