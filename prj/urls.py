from django.contrib import admin
from dynamo.api.router import router
from django.views.generic import TemplateView
from dynamo.api.views import DynamicModelViewSet
from prj.api.views import AuthView
from django.conf.urls import patterns, include, url

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="page/index.html"), name='home'),
    url(r'^api/', include(router.urls)),
    # url(r'^api/dynamicmodel/$', DynamicModelViewSet.as_view(), name='dynomo-list'),
    url(r'^api/auth/$', AuthView.as_view(), name='authenticate'),
    url(r'^admin/', include(admin.site.urls)),
)
