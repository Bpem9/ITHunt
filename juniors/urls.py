from django.contrib import admin
from django.urls import path, include
from .views import *
from .forms import *

urlpatterns = [

    path('reg/', RegisterJunior.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', userlogout, name='logout'),
    path('profile/<slug:jun_slug>/', JuniorProfile.as_view(), name='profile'),
    path('update/<slug:jun_slug>/', JuniorUpdate.as_view(), name='update'),
    path('<slug:pos_slug>/', JuniorsPosition.as_view(), name='position'),
    path('<slug:pos_slug>/<slug:jun_slug>/', JuniorPage.as_view(), name='junior'),
]