from Session import Session

import unittest
import argparse
import sqlalchemy
import pandas as pd

class tests(unittest.TestCase):

    def setUp(self, host):
        self.sess = Session('test', 'test', host, 'Test')

    def test_connect(self):
        assert(not self.sess.conn.closed)
        print('Connect success')

    def test_insert(self):
        try:
            self.sess.insert('test_table', ['column1', 'column2'], [['6/19/2020', 'test']], False)
            print('insert success')
        except sqlalchemy.exc.SQLAlchemyError as e:
            print('Insert Error: ', e)
            quit()

    def test_insert_CSV(self):
        try:
            self.sess.insert_from_CSV('./TestDocs/test.csv', 'test_table', True)
            print('csv success')
        except sqlalchemy.exc.SQLAlchemyError as e:
            print('CSV Error: ', e)
            quit()

    def test_execute_SQL(self):
        try:
            self.sess.execute_SQL('./queries/test.sql')
            print('sql_success')
        except sqlalchemy.exc.SQLAlchemyError as e:
            print('SQL Error: ', e)
            quit()

    def test_create_table(self):
        df = pd.read_csv('./TestDocs/test.csv')
        types=[]
        for item in df.iloc[0]:
            types.append(type(item))

        try:
            self.sess.create_table('test_create', list(df.columns), types)
            print('Table creation success')
        except sqlalchemy.exc.SQLAlchemyError as e:
            print('Create table error: ', e)
            quit()

    def test_insert_CSV_create_table(self):
        df = pd.read_csv('./TestDocs/test_create_insert.csv')
        types=[]
        for item in df.iloc[0]:
            types.append(type(item))

        try:
            self.sess.insert_from_CSV('./TestDocs/test_create_insert.csv', 'test_create_from_insert', True)
            self.sess.conn.execute("""DROP TABLE test_create_from_insert""")
        except sqlalchemy.exc.SQLAlchemyError as e:
            print('Insert and create error: ', e)
            quit()

    def test_insert_dir(self):
        try:
            self.sess.insert_directory('./TestDocs/dir/', 'test_dir_insert', True)
        except:
            print('Error inserting directory')

    def test_select(self):
        result = self.sess.select(['test_table'], conditions={'column1': ('test_table', '==', '6/19/2020')})
        assert result[0][0] == '6/19/2020'
    def test_execute_query(self):
        result = self.sess.execute_query("SELECT * FROM `Test`.`test_csvsql` LIMIT 1000;").fetchone()
        print(result)
        assert result[1] == '6/19/2020'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='Host IP for test')
    args = parser.parse_args()

    test = tests()

    test.setUp(args.host)
    test.test_connect()
    test.test_insert()
    test.test_insert_CSV()
    test.test_execute_SQL()
    test.test_create_table()
    test.test_insert_CSV_create_table()
    test.test_select()
    test.test_execute_query()
    print('Test SUCCESS')