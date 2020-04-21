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
        with open('account/project_dataset_sp2020_v1.1/Professors.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)

            for row in reader:

                try:
                    user = User.objects.get(email=row[1])
                except User.DoesNotExist:
                    user = User.objects.create_user(
                        first_name=row[0].split()[1],
                        last_name=row[0].split()[2],
                        email=row[1],
                        username=row[1],
                        password=row[2],
                    )

                print("User saved/created")
                department, _ = Department.objects.get_or_create(
                    name=row[7],
                    title=row[5]
                )

                print("Department saved/created")
                instructor, _ = FacultyMember.objects.get_or_create(
                    auth_user=user,
                    office_address=row[6],
                    department=department,
                    title=row[8],
                    age=row[3],
                    gender=row[4]
                )
                print("Instructor saved/created")

                teaching_team, _ = TeachingTeam.objects.get_or_create(team_id=row[9])
                teaching_team.instructor.add(instructor)
                print("Team saved/created")

                course, _ = Course.objects.get_or_create(number=row[10])
                print("Course saved/created")

                section1, created = Section.objects.get_or_create(
                    course=course,
                    number=1
                )
                print("Section saved/created")

                offering1, _ = Offering.objects.get_or_create(
                    section=section1,
                    teaching_team=teaching_team
                )
                print("Offering saved/created")

                section2, created = Section.objects.get_or_create(
                    course=course,
                    number=2
                )
                print("Section2 saved/created")

                offering2, _ = Offering.objects.get_or_create(
                    section=section2,
                    teaching_team=teaching_team
                )
                print("Offering2 saved/created")


