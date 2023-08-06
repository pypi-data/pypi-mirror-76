import argparse
import os
from . import Session

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user', help='user for database login')
    parser.add_argument('password', default=None, help='password for login if necessary')
    parser.add_argument('host', help='host IP for database')
    parser.add_argument('database', help='database to run queries on')
    parser.add_argument('table', help='table to insert into (will create new if doesn\'t exist)')
    parser.add_argument('filepath', help='filepath of CSV file to insert')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite already-present table in database')
    args = parser.parse_args()

    # create session for login
    sess = Session.Session(args.user, args.password, args.host, db=args.database)

    # if path is directory, insert entire directory, else insert specified file
    if os.path.isdir(args.filepath):
        sess.insert_directory(args.filepath, args.table, args.overwrite)
    else:
        sess.insert_from_CSV(args.filepath, args.table, args.overwrite)