from django.http import JsonResponse
from django.db.models import Prefetch, Q
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Enrollments, Post, Comment, Assignment, Student, Grade, Offering
from django.middleware.csrf import get_token
from django.utils import timezone
import json


@login_required(login_url='/login/')
def profile(request):
    person = request.user.student if getattr(request.user, 'student', None) else request.user.facultymember
    return JsonResponse({
        'Result': {
            'firstName': request.user.first_name,
            'lastName': request.user.last_name,
            'email': request.user.email,
            'age': person.age,
            'gender': person.gender
        }
    })


@login_required(login_url='/login/')
def course_info(request):
    enrollments = Enrollments.objects.select_related(
        'offering__section__course',
        'offering__teaching_team'
    ).prefetch_related(
        Prefetch(
            'offering__teaching_team__instructor',
            to_attr='instructors'
        ),
        Prefetch(
            'offering__teaching_team__ta',
            to_attr='tas'
        )
    ).filter(
        Q(students__auth_user=request.user) |
        Q(offering__teaching_team__instructor__auth_user=request.user)
    ).distinct()

    return JsonResponse({
        'Result': [{
            'id': enrollment.offering.id,
            'section': enrollment.offering.section.number,
            'course': {
                'id': enrollment.offering.section.course.id,
                'number': enrollment.offering.section.course.number,
                'name': enrollment.offering.section.course.name,
                'credit': enrollment.offering.section.course.credit,
            },
            'role': {
                'is_ta': enrollment.offering.teaching_team.ta.filter(auth_user=request.user).exists(),
                'is_student': enrollment.students.filter(auth_user=request.user).exists(),
                'is_instructor': enrollment.offering.teaching_team.instructor.filter(auth_user=request.user).exists()
            },
            'teaching_team': {
                'instructors': [{
                    'id': prof.id,
                    'name': prof.auth_user.first_name + ' ' + prof.auth_user.last_name,
                    'office': prof.office_address,
                    'email': prof.auth_user.email
                } for prof in enrollment.offering.teaching_team.instructors],
                'tas': [{
                    'id': ta.id,
                    'name': ta.auth_user.first_name + ' ' + ta.auth_user.last_name,
                    'email': ta.auth_user.email,
                } for ta in enrollment.offering.teaching_team.tas]

            }
        } for enrollment in enrollments]
    })


@login_required(login_url='/login/')
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
    ).filter(
        Q(students__auth_user=request.user) | 
        Q(offering__teaching_team__instructor__auth_user=request.user)
    ).distinct()

    return JsonResponse({
        'Result': [{
            'course': enrollment.offering.section.course.number,
            'section': enrollment.offering.section.number,
            'id': enrollment.offering.forum.id,
            'role': {
                'is_ta': enrollment.offering.teaching_team.ta.filter(auth_user=request.user).exists(),
                'is_student': enrollment.students.filter(auth_user=request.user).exists(),
                'is_instructor': enrollment.offering.teaching_team.instructor.filter(auth_user=request.user).exists()
            },
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


@login_required(login_url='/login/')
def create_post(request):
    try:
        data = json.loads(request.body)
        Post.objects.create(
            text=data['text'],
            forum_id=data['forum_id'],
            auth_user=request.user
        )
        return JsonResponse({
            'Result': 'Success'
        })
    except Exception as error:
        return JsonResponse({
            'Result': str(error) if error else 'Failure'
        })


@login_required(login_url='/login/')
def add_comment(request):
    try:
        data = json.loads(request.body)
        Comment.objects.create(
            text=data['text'],
            post_id=data['post_id'],
            auth_user=request.user
        )
        return JsonResponse({
            'Result': 'Success'
        })
    except Exception as error:
        return JsonResponse({
            'Result': str(error) if error else 'Failure'
        })


@login_required(login_url='/login/')
def create_assignment(request):
    try:
        data = json.loads(request.body)
        is_ta = lambda user: getattr(user, 'student', None) and user.student.is_ta
        is_faculty = lambda user: getattr(user, 'facultymember', None)
        if is_ta or is_faculty:
            assignment = Assignment.objects.create(
                name=data['name']
            )
            offering = Offering.objects.get(id=data['offering_id'])
            offering.assignment.add(assignment)
            offering.save()
            return JsonResponse({
                'Result': 'Success'
            })

        else:
            raise PermissionError
    except Exception as error:
        return JsonResponse({
            'Result': str(error) if error else 'Failure'
        })


@login_required(login_url='/login/')
def get_assignments(request):
    try:
        enrollments = Enrollments.objects.select_related(
            'offering'
        ).prefetch_related(
            Prefetch(
                'offering__assignment',
                to_attr='assignments'
            ),
            'offering__assignment__grade_set',
        ).filter(
            Q(students__auth_user=request.user) |
            Q(offering__teaching_team__instructor__auth_user=request.user),
            offering__assignment__isnull=False
        ).distinct()
        get_grade = lambda _id: (
            Grade.objects.filter(assignment_id=_id, student__auth_user=request.user).first().grade
            if Grade.objects.filter(assignment_id=_id, student__auth_user=request.user).exists()
            else "N/A"
        )
        return JsonResponse({
            'Result': [{
                'id': enrollment.id,
                'offering_id': enrollment.offering.id,
                'course': enrollment.offering.section.course.number,
                'section': enrollment.offering.section.number,
                'role': {
                    'is_ta': enrollment.offering.teaching_team.ta.filter(auth_user=request.user).exists(),
                    'is_student': enrollment.students.filter(auth_user=request.user).exists(),
                    'is_instructor': enrollment.offering.teaching_team.instructor.filter(auth_user=request.user).exists()
                },
                'assignments': [{
                    'id': assignment.id,
                    'name': assignment.name,
                    'number': assignment.number,
                    'grade': get_grade(assignment.id)
                } for assignment in enrollment.offering.assignments]
            } for enrollment in enrollments]
        })
    except Exception as error:
        return JsonResponse({
            'Result': str(error) if error else 'Failure'
        })


@login_required(login_url='/login/')
def drop_course(request):
    try:
        data = json.loads(request.body)
        enrollment = Enrollments.objects.get(
            offering__section__course_id=data['course_id'],
            students__auth_user=request.user
        )
        if enrollment.offering.section.drop_deadline < timezone.now():
            raise PermissionError

        enrollment.students.remove(Student.objects.get(auth_user=request.user))

        # Delete posts and comments
        posts = Post.objects.filter(auth_user=request.user)
        Comment.objects.filter(post__in=posts).delete()
        Comment.objects.filter(auth_user=request.user).delete()
        posts.delete()

        return JsonResponse({
            'Result': 'Success'
        })
    except Exception as error:
        print(error)
        return JsonResponse({
            'Result': 'Cannot Drop Course. Deadline Passed'
        })


@login_required(login_url='/login/')
def submit_scores(request):
    try:
        data = json.loads(request.body)
        is_ta = lambda user: getattr(user, 'student', None) and user.student.is_ta
        is_faculty = lambda user: getattr(user, 'facultymember', None)
        if is_ta or is_faculty:
            Grade.objects.create(
                assignment_id=data['assignment_id'],
                student_id=data['student_id'],
                grade=int(data['grade'])
            )
            return JsonResponse({
                'Result': 'Success'
             })
        else:
            raise PermissionError
    except Exception as error:
        return JsonResponse({
            'Result': str(error) if error else 'Failure'
        })


@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


@login_required(login_url='/login/')
def csrf_token(request):
    return JsonResponse({
        'Result': get_token(request)
    })


@login_required(login_url='/login/')
def get_status(request):
    is_faculty = True
    if hasattr(request.user, 'student'):
        is_faculty = request.user.student.is_ta
    return JsonResponse({
        'Result': is_faculty
    })


@login_required(login_url='/login/')
def get_class(request):
    enrollments = Enrollments.objects.select_related(
            'offering'
        ).prefetch_related(
            Prefetch(
                'offering__assignment',
                to_attr='assignments'
            ),
            'students'
        ).filter(
            Q(offering__teaching_team__ta__auth_user=request.user) |
            Q(offering__teaching_team__instructor__auth_user=request.user),
        ).distinct()
    
    get_grade = lambda _id, user_id: (
            Grade.objects.filter(assignment_id=_id, student__auth_user_id=user_id).first().grade
            if Grade.objects.filter(assignment_id=_id, student__auth_user_id=user_id).exists()
            else "N/A"
        )
    
    return JsonResponse({
            'Result': [{
                'id': enrollment.id,
                'offering_id': enrollment.offering.id,
                'course': {
                    'number': enrollment.offering.section.course.number,
                    'name': enrollment.offering.section.course.name,
                },
                'section': enrollment.offering.section.number,
                'students': [{
                    'id': student.id,
                    'first_name': student.auth_user.first_name,
                    'last_name': student.auth_user.last_name,
                    'email': student.auth_user.email,
                    'assignments': [{
                        'id': assignment.id,
                        'grade': get_grade(assignment.id, student.auth_user_id)
                    } for assignment in sorted(enrollment.offering.assignments, key=lambda x: x.id)]
                } for student in enrollment.students.all()],
                'role': {
                    'is_ta': enrollment.offering.teaching_team.ta.filter(auth_user=request.user).exists(),
                    'is_student': enrollment.students.filter(auth_user=request.user).exists(),
                    'is_instructor': enrollment.offering.teaching_team.instructor.filter(auth_user=request.user).exists()
                },
                'assignments': [{
                    'id': assignment.id,
                    'name': assignment.name,
                    'number': assignment.number,
                } for assignment in sorted(enrollment.offering.assignments, key=lambda x: x.id)]
            } for enrollment in enrollments]
        })
    