from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
import logging

from cmuaudit.service import parse_audit


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


@login_required
@csrf_protect
def upload(request, template_name="cmuaudit/upload.jinja"):
    context = {}

    if request.method == "POST":
        audit_text = request.POST['audit_text']
        context['audit_data'] = parse_audit(audit_text)
        logger.debug(context['audit_data'])
        template_name = "cmuaudit/upload.completed.jinja"

    return render(request, template_name, context)


@login_required
def save_audit(request, template_name="cmuaudit/save_audit.jinja"):
    context = {}

    year_arr = request.POST.getlist('year', [])
    course_id_arr = request.POST.getlist('course_id', [])
    season_arr = request.POST.getlist('season', [])
    unit_arr = request.POST.getlist('unit', [])
    grade_arr = request.POST.getlist('grade', [])

    audit_data = [
        {
            "year": year,
            "course_id": course_id,
            "season": season,
            "unit": unit,
            "grade": grade
        } for (year, course_id, season, unit, grade)
          in zip(year_arr, course_id_arr, season_arr, unit_arr, grade_arr)
    ]

    logging.debug(json.dumps(audit_data))


    return render(request, template_name, context)
