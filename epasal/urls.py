"""epasal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.conf.urls.static import static
from django.conf import settings

from shop.views import Homepage, ProductView, CartView, CategoryView, CategoryAPI
from cms.views import SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Homepage.as_view(), name='homepage'),
    path('product/<int:product_id>', ProductView.as_view(), name='product_page'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup', SignUpView.as_view(), name='signup'),
    path('cart/<int:product_id>', CartView.as_view(), name='cart_page'),
    path('categoty/<int:category_id>', CategoryView.as_view(), name='category_page'),
    path('api/categories', CategoryAPI.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
