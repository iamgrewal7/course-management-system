from django.contrib import admin
from .models import *


class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ('name', 'number', 'credit')
    raw_id_fields = ['pre_req']
    search_fields = ['name']


class SectionAdmin(admin.ModelAdmin):
    model = Section
    list_display = ('number', 'course', 'limit')
    raw_id_fields = ['course']
    search_fields = ['name']


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


class FacultyMemberAdmin(admin.ModelAdmin):
    raw_id_fields = ['auth_user']
    list_display = ('department', 'auth_user', 'office_address')
    search_fields = ['auth_user__username', 'auth_user__first_name', 'auth_user__last_name']


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('info',)


class TeachingTeamAdmin(admin.ModelAdmin):
    raw_id_fields = ['instructor', 'ta']


class OfferingAdmin(admin.ModelAdmin):
    raw_id_fields = ['section', 'assignment', 'announcement', 'teaching_team']


class EnrollmentsAdmin(admin.ModelAdmin):
    raw_id_fields = ['offering', 'students']


class GradeAdmin(admin.ModelAdmin):
    list_display = ('grade',)
    raw_id_fields = ['student', 'assignment']


class StudentAdmin(admin.ModelAdmin):
    model = Student
    list_display = ('student_id', 'auth_user', 'is_ta')
    list_filter = ('is_ta', 'major')
    raw_id_fields = ['auth_user', 'major']
    search_fields = ['auth_user__username', 'auth_user__first_name', 'auth_user__last_name']


class ForumAdmin(admin.ModelAdmin):
    model = Forum
    raw_id_fields = ['offering']


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['forum', 'comment']
    raw_id_fields = ['forum', 'comment', 'auth_user']


admin.site.register(Course, CourseAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(FacultyMember, FacultyMemberAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Offering, OfferingAdmin)
admin.site.register(Enrollments, EnrollmentsAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(TeachingTeam, TeachingTeamAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Post, PostAdmin)
