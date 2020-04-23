import csv
from account.models import *
from django.core.management.base import BaseCommand
from random import choice
from string import ascii_lowercase, digits


def generate_random_username(length=16, chars=ascii_lowercase + digits, split=4, delimiter='-'):
    username = ''.join([choice(chars) for _ in range(length)])

    if split:
        username = delimiter.join([username[start:start + split] for start in range(0, len(username), split)])

    try:
        User.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except User.DoesNotExist:
        return username


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('account/project_dataset_sp2020_v1.1/Students_TA.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)

            for row in reader:

                try:
                    user = User.objects.get(email=row[1])
                except User.DoesNotExist:
                    user = User.objects.create_user(
                        first_name=row[0].split()[0],
                        last_name=row[0].split()[1],
                        email=row[1],
                        username=row[1],
                        password=row[8],
                    )
                print("User saved/created")

                student, _ = Student.objects.get_or_create(
                    student_id=user.username,
                    auth_user=user,
                    zipcode=row[3],
                    gender=row[5],
                    city=row[6],
                    state=row[7],
                    age=row[2],
                    street=row[9]
                )
                print("Student saved/created")

                if row[44]:
                    teaching_team, _ = TeachingTeam.objects.get_or_create(team_id=int(float(row[44])))
                    teaching_team.ta.add(student)
                    print("Team saved/created")

                #############################################################################
                # Course 1
                course = Course.objects.get(number=row[11])
                course.name = row[12]
                course.save()
                print("Course1 saved/created")

                section = Section.objects.get(
                    course=course,
                    number=int(float(row[14])),
                )
                section.limit = row[15]
                section.save()
                offering = Offering.objects.get(
                    section=section
                )
                print("Section1 saved/created")

                # HW1
                assignment, _ = Assignment.objects.get_or_create(
                    number=int(float(row[16])),
                    name=row[17]
                )

                offering.assignment.add(assignment)
                offering.save()

                # HW1 Grade
                grade, _ = Grade.objects.get_or_create(
                    assignment=assignment,
                    student=student,
                    grade=row[18]
                )



                # EXAM 1
                if row[19]:
                    assignment, _ = Assignment.objects.get_or_create(
                        number=int(float(row[19])),
                        name=row[20]
                    )

                    offering.assignment.add(assignment)
                    offering.save()

                    # Exam 1 grade
                    grade, _ = Grade.objects.get_or_create(
                        assignment=assignment,
                        student=student,
                        grade=row[21]
                    )



                enrollment, _ = Enrollments.objects.get_or_create(offering=offering)
                enrollment.students.add(student)
                enrollment.save()

                #############################################################################

                #############################################################################
                # Course 2
                course = Course.objects.get(number=row[22])
                course.name = row[23]
                course.save()
                print("Course1 saved/created")

                section = Section.objects.get(
                    course=course,
                    number=int(float(row[25])),
                )
                section.limit = row[26]
                section.save()
                print("Section1 saved/created")
                offering = Offering.objects.get(
                    section=section
                )

                # HW1
                assignment, _ = Assignment.objects.get_or_create(
                    number=int(float(row[27])),
                    name=row[28]
                )
                offering.assignment.add(assignment)
                offering.save()

                # HW1 Grade
                grade, _ = Grade.objects.get_or_create(
                    assignment=assignment,
                    student=student,
                    grade=row[29]
                )

                # EXAM 1
                if row[30]:
                    assignment, _ = Assignment.objects.get_or_create(
                        number=int(float(row[30])),
                        name=row[31]
                    )
                    offering.assignment.add(assignment)
                    offering.save()

                    # Exam 1 grade
                    grade, _ = Grade.objects.get_or_create(
                        assignment=assignment,
                        student=student,
                        grade=row[32]
                    )

                
                enrollment, _ = Enrollments.objects.get_or_create(offering=offering)
                enrollment.students.add(student)
                enrollment.save()
                #############################################################################

                #############################################################################
                # Course 3
                course = Course.objects.get(number=row[33])
                course.name = row[34]
                course.save()
                print("Course1 saved/created")

                section = Section.objects.get(
                    course=course,
                    number=int(float(row[36])),
                )
                section.limit = row[37]
                section.save()
                print("Section1 saved/created")
                offering = Offering.objects.get(
                    section=section
                )


                # HW1
                assignment, _ = Assignment.objects.get_or_create(
                    number=int(float(row[38])),
                    name=row[39]
                )
                offering.assignment.add(assignment)
                offering.save()

                # HW1 Grade
                grade, _ = Grade.objects.get_or_create(
                    assignment=assignment,
                    student=student,
                    grade=row[40]
                )

                # EXAM 1
                if row[41]:
                    assignment, _ = Assignment.objects.get_or_create(
                        number=int(float(row[41])),
                        name=row[42]
                    )
                    offering.assignment.add(assignment)
                    offering.save()

                    # Exam 1 grade
                    grade, _ = Grade.objects.get_or_create(
                        assignment=assignment,
                        student=student,
                        grade=row[43]
                    )

                
                
                enrollment, _ = Enrollments.objects.get_or_create(offering=offering)
                enrollment.students.add(student)
                enrollment.save()
                #############################################################################

