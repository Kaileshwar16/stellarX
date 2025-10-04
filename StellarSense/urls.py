"""StellarSense URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from home.views import signup_view  # ✅ Add this line

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs
    path('', include('home.urls')),
    path('observations/', include('observations.urls')),
    path('crowdfunding/', include('crowdfunding.urls')),
    path('profile/', include('profiles.urls')),
    path('calender/', include('calender.urls')),
    path('gravity_simulation/', include('gravity_simulation.urls')),

    # Auth
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/signup/', signup_view, name='signup'),
    path('space-tracker/', include('space_tracker.urls', namespace='space_tracker')),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Media file handling (for uploaded images)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
