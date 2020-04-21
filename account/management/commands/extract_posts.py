import csv
from account.models import *
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('account/project_dataset_sp2020_v1.1/Posts_Comments.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)

            for row in reader:
                offerings = Offering.objects.filter(
                    section__course__number=row[0]
                )
                for offering in offerings:
                    offering.section.drop_deadline = parse_date(row[1])
                    offering.section.save()
                    forum = Forum.objects.create(offering=offering)

                    if row[2]:
                        post = Post.objects.create(
                            forum=forum,
                            auth_user=User.objects.get(email=row[3]),
                            text=row[2],
                        )

                        if row[4]:
                            Comment.objects.create(
                                auth_user=User.objects.get(email=row[5]),
                                text=row[4],
                                post=post
                            )
