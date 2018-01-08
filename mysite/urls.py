"""mysite URL Configuration

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
from django.conf.urls import url
from django.urls import path, include, re_path          #new in Django2
from django.contrib import admin
from blog import views as bv
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as av

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', av.login, name="login"),           #name attrib is set for HTML use, e.g. {% url 'blog' %}
    path('logout/', bv.logout, name="logout"),
    url('', include('social_django.urls', namespace='social')),
    path('register/', bv.register, name='register'),
    path('', bv.blogindex, name="blog"),                         
    path('blog/<int:key>/', bv.post_page, name="page"),
    path('post/', bv.post_new, name="post_new"),
    path('post_tag/<key>/', bv.post_tag, name="post_tag"),
    path('password_reset', av.password_reset, name='password_reset'),
    path('password_reset_done', av.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', av.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', av.password_reset_complete, name='password_reset_complete'),
    path('change_password/', av.password_change, name='password_change'),
    path('change_password/done/', bv.changepassworddone, name='password_change_done'),
    path('myaccount/', bv.useraccount, name='myaccount'),
    path('archives/', bv.archives, name='archives')
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

