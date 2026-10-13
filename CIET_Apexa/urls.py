"""
URL configuration for CIET_Apexa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.urls import path
from myapp import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.contrib.auth import logout

urlpatterns = [
    path("admin/", admin.site.urls),
    path('base/',views.base,name='base'),
    path('index/',views.index,name='index'),
    path('login/',views.user_login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('post/', views.post, name='post'),
    path('fields/', views.fields, name='fields'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile_view/<int:user_id>/', views.profile_view, name='profile_view'),
    # Club URLs
    path('add-club/', views.add_club, name='add_club'),
    path('club_list/', views.club_list, name='club_list'),

    # Startup URLs
    path('add-startup/', views.add_startup, name='add_startup'),
    path('startups/', views.startup_list, name='startup_list'),

    path('startup/<int:id>/', views.startup_detail, name='startup_detail'),

    # path('upload/', views.upload_story, name='upload_story'),

    path('dep/', views.dep, name='dep'),
    path('dep_list/', views.dep_list, name='dep_list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
