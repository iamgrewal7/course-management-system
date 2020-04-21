from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Enrollments
from django.shortcuts import render
import json


def profile(request):
    return render(request, 'profile.html')


def course_info(request):
    enrollments = Enrollments.objects.filter(students__auth_user=request.user)
    return JsonResponse({
        'Result': [{
            'section': enrollment.offering.section.number,
            'course': {
                'number': enrollment.offering.section.course.number,
                'name': enrollment.offering.section.course.name,
                'credit': enrollment.offering.section.course.credit,
            },
            'teaching_team': {
                'instructors': [{
                    'name': prof.auth_user.first_name + ' ' + prof.auth_user.last_name,
                    'office': prof.office_address,
                    'email': prof.auth_user.email
                } for prof in enrollment.offering.teaching_team.instructor.all()],
                'tas': [{
                    'name': ta.auth_user.first_name + ' ' + ta.auth_user.last_name,
                    'email': ta.auth_user.email,
                } for ta in enrollment.offering.teaching_team.ta.all()]

            }
        } for enrollment in enrollments]
    })


