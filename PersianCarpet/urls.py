from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView
from .views import ContactView, ProductListView

admin.autodiscover()

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    path('', TemplateView.as_view(template_name='home/m_index.html'), name='home'),
    path('home/', TemplateView.as_view(template_name='home/index.html'), name='home-slider'),
    path('home-video/', TemplateView.as_view(template_name='home/m_index.html'), name='home-video'),
    path('products/', ProductListView.as_view(), name='products'),
    path('about-us/', TemplateView.as_view(template_name='about-us/m_index.html'), name='about'),
    path('contact-us/', ContactView.as_view(), name='contact'),
]


urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("cms.urls")),
    prefix_default_language=False,
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
