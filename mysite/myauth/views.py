from random import random

from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.utils.translation import gettext_lazy as _, ngettext
from django.views.decorators.cache import cache_page

from myauth.models import Profile
from myauth.forms import ProfileForm


class HelloView(View):
    welcome_message = _('welcome hello World!')

    def get(self, request):
        items_str = request.GET.get('items') or 0
        items = int(items_str)
        products_line = ngettext(
            'one product',
            '{count} products',
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f'<h1>{self.welcome_message}</h1>'
            f'\n<h2>{products_line}</h2>',
        )


class AboutMeView(TemplateView):
    template_name = 'myauth/about-me.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            profile = None
        context['profile'] = profile
        return context


class UpdateAboutMeView(UpdateView):
    model = Profile
    template_name = 'myauth/about-me_update_form.html'
    form_class = ProfileForm
    success_url = reverse_lazy('myauth:about-me')


class UserListView(ListView):
    model = Profile
    template_name = 'myauth/user_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.all()


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)

        return response


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/admin/')

        return render(request, 'myauth/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin/')

    return render(request, 'myauth/login.html', {'error': 'Invalid login credentials'})


def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse("myauth:login"))


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_superuser:
        response = HttpResponse('Cookie set')
        response.set_cookie('fizz', 'buzz', max_age=3600)
        return response
    else:
        return HttpResponse('Unauthorized', status=401)


@cache_page(60 * 2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value: {value!r} + {random()}')


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse("Session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'Session value: {value!r}')


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})
