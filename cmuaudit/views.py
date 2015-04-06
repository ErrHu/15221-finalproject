import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

logger = logging.getLogger(__name__)


def home(request):
    template_name = "cmuaudit/index.anonymous.jinja"
    return render(request, template_name, {})


@csrf_protect
def sign_in(request, template_name="cmuaudit/sign_in.anonymous.jinja"):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return HttpResponseRedirect(next_url)

    return render(request, template_name, {})


@csrf_protect
def sign_up(request, template_name="cmuaudit/sign_up.anonymous.jinja"):
    logger.error(request.method)
    logger.error("request.POST")
    logger.error(request.POST)
    logger.error("request.GET")
    logger.error(request.GET)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
        except Exception, e:
            pass
        else:
            return HttpResponseRedirect("/")

    return render(request, template_name, {})
