from django.db import models
from django.contrib.auth.models import User


GENDER_CHOICES = [
    ('M', 'Female'),
    ('F', 'Male')
]


class UserDetail(models.Model):
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)
    age = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=1)


class Course(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=10, unique=True, null=True)
    pre_req = models.ManyToManyField('self', blank=True)
    credit = models.PositiveIntegerField(default=3)


class Section(models.Model):
    number = models.PositiveIntegerField(default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    limit = models.IntegerField(default=50)
    drop_deadline = models.DateTimeField(null=True)


class Department(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=10, null=True)


class Student(UserDetail):
    student_id = models.CharField(max_length=10, unique=True)
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.ManyToManyField(Department, blank=True)
    is_ta = models.BooleanField(default=False)


class FacultyMember(UserDetail):
    title = models.CharField(max_length=10, null=True)
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    office_address = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


class Assignment(models.Model):
    number = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=50)


class Grade(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.FloatField(default=0)


class Announcement(models.Model):
    info = models.CharField(max_length=100)


class TeachingTeam(models.Model):
    team_id = models.IntegerField(unique=True, null=True)
    instructor = models.ManyToManyField(FacultyMember, blank=True)
    ta = models.ManyToManyField(Student, blank=True)


class Offering(models.Model):
    section = models.OneToOneField(Section, on_delete=models.CASCADE)
    assignment = models.ManyToManyField(Assignment, blank=True)
    announcement = models.ManyToManyField(Announcement, blank=True)
    teaching_team = models.ForeignKey(TeachingTeam, null=True, on_delete=models.CASCADE)


class Enrollments(models.Model):
    offering = models.OneToOneField(Offering, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)


class Forum(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE)


class Post(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    comment = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
