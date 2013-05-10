from fabric.api import task, local

from ylio.config import PG_HOST, PG_PORT, DB_NAME, PG_USER


def run_pg_command(command, user=PG_USER, db=DB_NAME, host=PG_HOST, port=PG_PORT):
    if db is None:
        full_command = 'psql -U {user} -h {host} -p {port} -c "{command}"'
    else:
        full_command = 'psql -U {user} -d {db} -h {host} -p {port} -c "{command}"'

    local(full_command.format(**locals()))


@task
def create_db(drop=False):
    """
    Creates a database using the values in ylio.config
    """

    if drop:
        print 'Dropping existing database...'
        run_pg_command('DROP DATABASE IF EXISTS {0}'.format(DB_NAME), db=None)

    print 'Creating database: {0}:{1}/{2}'.format(PG_HOST, PG_PORT, DB_NAME)
    command = "CREATE DATABASE {0} OWNER {1} ENCODING 'UTF8'".format(DB_NAME, PG_USER)
    run_pg_command(command, db=None)

    print 'Applying schema.sql'
    command = 'psql -U {0} -h {1} -p {2} -d {3} < schema.sql'
    local(command.format(PG_USER, PG_HOST, PG_PORT, DB_NAME))

    print 'Finished'


@task
def recreate_db():
    """
    The same as create_db, but drops the exiting one first
    """
    create_db(drop=True)
