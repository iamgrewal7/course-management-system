from django.http import JsonResponse
from django.db.models import Prefetch
from .models import Enrollments, Post


def profile(request):
    person = request.user.student if getattr(request.user, 'student') else request.user.facultymember
    return JsonResponse({
        'Result': {
            'firstName': request.user.first_name,
            'lastName': request.user.last_name,
            'email': request.user.email,
            'age': person.age,
            'gender': person.gender
        }
    })


def course_info(request):
    enrollments = Enrollments.objects.filter(students__auth_user=request.user)
    return JsonResponse({
        'Result': [{
            'section': enrollment.offering.section.number,
            'course': {
                'id': enrollment.offering.section.course.id,
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


def get_forum(request):
    enrollments = Enrollments.objects.select_related(
        'offering__forum',
        'offering__section__course'
    ).prefetch_related(
        Prefetch(
            'offering__forum__post_set',
            Post.objects.prefetch_related(
                Prefetch(
                    'comment_set',
                    to_attr='comments'
                )
            ),
            to_attr='posts'
        )
    ).filter(students__auth_user=request.user)

    return JsonResponse({
        'Result': [{
            'course': enrollment.offering.section.course.number,
            'id': enrollment.offering.forum.id,
            'posts': [{
                'id': post.id,
                'text': post.text,
                'by': post.auth_user.email,
                'comments': [{
                    'id': comment.id,
                    'text': comment.text,
                    'by': comment.auth_user.email
                } for comment in post.comments]
            } for post in enrollment.offering.forum.posts]
        } for enrollment in enrollments]
    })



