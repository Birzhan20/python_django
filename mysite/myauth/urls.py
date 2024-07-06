from django.urls import path
from django.contrib.auth.views import LoginView

from .views import (
    get_cookie_view,
    set_cookie_view,
    get_session_view,
    set_session_view,
    logout_view,
    AboutMeView,
    RegisterView,
    FooBarView,
    UpdateAboutMeView,
)


app_name = 'myauth'

urlpatterns = [
    path('login/',
         LoginView.as_view(
             template_name= 'myauth/login.html',
             redirect_authenticated_user=True,
         ),
         name='login'),
    path('logout/', logout_view, name='logout'),
    path('cookie/get/', get_cookie_view, name='cookie-get'),
    path('cookie/set/', set_cookie_view, name='cookie-set'),

    path('session/set/', set_session_view, name='session-set'),
    path('session/get/', get_session_view, name='session-get'),
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('about-me/update/<int:pk>', UpdateAboutMeView.as_view(), name='about-me_update_form'),

    path('register/', RegisterView.as_view(), name='register'),

    path('foo-bar/', FooBarView.as_view(), name='foo-bar'),
]
