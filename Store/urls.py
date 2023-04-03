"""Store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from posts.views import hello_view, now_date_view, goodbye_view, main_view, products_view, product_detail_view, \
    product_create_view
from Store import settings
from django.conf.urls.static import static
from users.views import register_view, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_view),
    path('now_date/', now_date_view),
    path('goodbye/', goodbye_view),
    path('', main_view),
    path('products/', products_view),
    path('products/<int:id>/', product_detail_view),
    path('products/create/', product_create_view),

    path('users/register/', register_view),
    path('users/login/', login_view),
    path('users/logout', logout_view)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
