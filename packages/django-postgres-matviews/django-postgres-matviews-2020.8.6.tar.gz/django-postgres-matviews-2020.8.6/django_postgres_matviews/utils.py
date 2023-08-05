from django.db import connection

SQL = """
SELECT format('%s.%s',schemaname,matviewname)
FROM pg_matviews
ORDER BY format('%s.%s',schemaname,matviewname)
"""


def get_matviews():
    cursor = connection.cursor()
    cursor.execute(SQL)
    return list(map(lambda r: r[0], cursor.fetchall()))


def drop_matviews():
    cursor = connection.cursor()
    for matview in get_matviews():
        schemaname, matviewname = matview.split('.')
        sql = """DROP MATERIALIZED VIEW IF EXISTS "%s"."%s" CASCADE;""" % (
            schemaname, matviewname)
        cursor.execute(sql)


def refresh_matviews(print_sql=None):
    cursor = connection.cursor()
    for matview in get_matviews():
        schemaname, matviewname = matview.split('.')
        sql = 'REFRESH MATERIALIZED VIEW "%s"."%s"' % (schemaname, matviewname)
        cursor.execute(sql)
