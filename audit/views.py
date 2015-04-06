import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from audit.models import UserAudit
from audit.services import parse_audit

logger = logging.getLogger(__name__)


@login_required
@csrf_protect
def upload(request, template_name="audit/upload.jinja"):
    context = {}

    if request.method == "POST":
        audit_text = request.POST['audit_text']
        context['audit_data'] = parse_audit(audit_text)
        logger.debug(context['audit_data'])
        template_name = "audit/upload.completed.jinja"

    return render(request, template_name, context)


@login_required
def save_audit(request, template_name="audit/save_audit.jinja"):
    context = {}

    if not request.method == 'POST':
        return HttpResponseForbidden()

    year_arr = request.POST.getlist('year', [])
    course_id_arr = request.POST.getlist('course_id', [])
    season_arr = request.POST.getlist('season', [])
    unit_arr = request.POST.getlist('unit', [])
    grade_arr = request.POST.getlist('grade', [])

    merged_list = zip(
        year_arr,
        course_id_arr,
        season_arr,
        unit_arr,
        grade_arr
    )

    audit_data = [
        {
            "year": year,
            "course_id": course_id,
            "season": season,
            "unit": unit,
            "grade": grade
        } for (year, course_id, season, unit, grade) in merged_list
    ]

    audit_data_text = json.dumps(audit_data)

    user_audit, created = UserAudit.objects.get_or_create(
        user=request.user,
        defaults={'audit': audit_data_text}
    )

    if not created:
        user_audit.audit = audit_data_text
        user_audit.save()

    return HttpResponseRedirect("/")
