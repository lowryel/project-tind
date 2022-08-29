from django.conf import settings
from django.urls import path, include
from tinda import views

urlpatterns = [
    path('', views.home, name='home'),
    path('comments/<pk>', views.commentPost, name='comment'),
    path('details/', views.galleryview, name='details'),
    path('login', views.loginPage, name='login'),
    path('register', views.registerUser, name='register'),
    path('new_tinda', views.NewTindaCreateView.as_view(), name='new-tinda'),
    path('logout', views.lougoutUser, name='logout')
]
