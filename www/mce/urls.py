"""mce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from django.conf.urls import url
from django.contrib import admin

from home import views as home_views
from home.render import Render as pdf_view

# from django.conf.urls import patterns, include
# from dbadmin.admin import admin_site
from django.contrib import admin
from adminplus.sites import AdminSitePlus

admin.site = admin.sites.site = AdminSitePlus()
admin.site.site_header = 'Database Administration - Olivet Military Course Equivalency'
admin.site.index_title = 'Olivet MCE Database'
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_views.index, name='home'),
    url(r'^pdf_processing', home_views.pdf_processing, name='pdf_processing'),
    url(r'^course_processing', home_views.course_processing, name='course_processing'),
    url(r'^course_information_pdf_processing', home_views.course_information_pdf_processing, name='course_information_pdf_processing'),
    url(r'^multiform', home_views.multi_form, name='multiform'),
    url(r'^result', home_views.result, name='result'),
    url(r'^pdf', pdf_view.render, name='render')



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()












