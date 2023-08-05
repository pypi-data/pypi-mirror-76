from django.core.management.base import BaseCommand
from django.db import connection

from django_postgres_matviews.utils import get_matviews


class Command(BaseCommand):

    def handle(self, *args, **options):
        cursor = connection.cursor()
        for matview in get_matviews():
            schemaname, matviewname = matview.split('.')
            sql = """DROP MATERIALIZED VIEW IF EXISTS "%s"."%s" CASCADE;""" % (
                schemaname, matviewname)
            print(sql)
            cursor.execute(sql)
