"""
URL configuration for thursday1923 project.

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
# from django.contrib import admin
# from django.urls import path
# from thursdayapp import views
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path("register",views.register,name='register'),
#     path("login",views.user_login,name='user_login'),
#     path("home",views.home,name='home'),
#     path("place_order",views.place_order, name="place_order"),
#     path('index',views.index,name="index"),
#     path('details',views.details,name='details'),
#     path('user_logout',views.user_logout),
#     path('catfilter/<cv>',views.catfilter),
#     path('sort/<sv>',views.sort),
#     path('range',views.range),
   
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path
from thursdayapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('home/', views.home, name='home'),
    path('', views.index, name='index'),
    path('details/', views.details, name='details'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('catfilter/<int:cv>/', views.catfilter, name='catfilter'),
    path('sort/<sv>/', views.sort, name='sort'),
    path('range/', views.range, name='range'),
    path("addtocart/<pid>",views.addtocart),
    path('viewcart',views.viewcart),
    path('remove/<int:cid>',views.remove),
    path('product_details/<pid>',views.product_details),
    path('contact',views.contact),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendmail',views.sendusermail),
    path('removes/<int:cid>/', views.removes, name='removes'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
