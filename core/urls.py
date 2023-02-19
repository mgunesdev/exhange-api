"""apps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='admin-home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='admin-home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path
from rest_framework_swagger.views import get_swagger_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


schema_view = get_swagger_view(title='EXCHANGE RATE API')

urlpatterns = []

urlpatterns += [
                   url(r'^router', include(router.urls)),
                   url(r'^proadmin', admin.site.urls),
                   url(r'^$', schema_view, name='api-doc'),
                   url(r'^api/v1/?', include('api.urls'), name='rest-api'),
               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
