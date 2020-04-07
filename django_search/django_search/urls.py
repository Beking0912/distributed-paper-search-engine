"""django_search URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import path
# from django.views.generic import TemplateView
from django.conf.urls import url
from search.views import SearchSuggest, SearchView, IndexView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^suggest/$', SearchSuggest.as_view(), name="suggest"),
    url(r'^search/$', SearchView.as_view(), name="search"),
]
