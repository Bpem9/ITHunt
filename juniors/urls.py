from django.contrib import admin
from django.urls import path, include
from .views import *
from .forms import *

urlpatterns = [
    path('<int:pos_id>/<slug:jun_slug>/', JuniorPage.as_view(), name='junior'),
    path('pos/<int:pos_id>/', JuniorsPosition.as_view(), name='position'),
    path('reg/', RegisterJunior.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', userlogout, name='logout'),
    path('profile/', JuniorProfile.as_view(), name='profile')
]