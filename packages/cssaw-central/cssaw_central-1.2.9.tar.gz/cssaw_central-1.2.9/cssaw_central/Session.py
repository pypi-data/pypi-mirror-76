import sqlalchemy as alc
import logging
import pandas as pd
import datetime as dt
import os

import operator

class Session:
    def __init__(self, user, password, host, db='Test'):
        """ Initialize connection to database

            args:
                user ---- name of user to connect as
                password ---- password for specified user
                host ---- host ip to connect to

            kwargs:
                db ---- database to connect to (defaults to Test)
        """
        self.engine = alc.create_engine("mysql+pymysql://{}:{}@{}/{}".format(user, password, host, db), echo=True)

        self.meta = alc.MetaData(self.engine)

        self.conn = self.engine.connect()

        self.type_dict = {float : alc.types.Float, int : alc.types.Integer, str : alc.types.String(length=50)}

    def execute_SQL(self, filename):
        """ execute .SQL file of commands 
        
            args:
                filename ---- path of file to execute (must be .sql)
        """

        # open file

        file = open(filename, 'r', encoding='utf-8-sig')
        sql = file.read()
        file.close()

        # get commands
        commands = sql.split(';')
        commands.pop()
        
        results = []

        # execute commands
        for command in commands:
            command = command.strip()
            try:
                results.append(self.conn.execute(alc.sql.text(command)))
            except:
                logging.error('Operation \"' + command + '\" failed, skipping...')

        return results

    def execute_query(self, command, pandas=False):
        """ execute one line sql commands 
        
            args:
                command ---- a one line sql query 

            kwargs:
                pandas ---- If true, return dataframe. If false, return resultproxy.
        """

        if pandas:
            return pd.read_sql(command, self.conn)
        else:
            return self.conn.execute(alc.sql.text(command))
        
    def insert(self, table, columns, rows, overwrite):
        """ insert given rows into given table.
            Creates table if it doesn't already exist.
        
            args:
                table ---- name of table to insert into
                columns ---- list of column names
                rows ---- list of lists of values to put into corresponding columns
                overwrite ---- bool denoting whether to overwrite or append to table

                len(columns) MUST EQUAL len(rows)
        """

        # determine if numpy or python type and convert accordingly
        types = []
        for item in rows[0]:
            if type(item).__module__ == 'numpy':
                types.append(type(item.item()))
            else:
                types.append(type(item))

        # create dataframe
        df = pd.DataFrame(data=rows, columns=columns)

        # if table doesn't exist, create
        if not self.engine.has_table(table):
            self.create_table(table, columns, types)
        
        # insert
        try:
            if overwrite:
                df.to_sql(table, self.engine, if_exists='replace', index=False)
            else:
                df.to_sql(table, self.engine, if_exists='append', index=False)
        except ValueError as e:
            print(e)
            quit()

    def insert_from_CSV(self, filename, table, overwrite):
        """ Inserts entire CSV file into specified table.
            Creates table if it doesn't already exist.

            args:
                filename ---- file path of data to upload
                table ---- name of table to insert into
                overwrite ---- bool denoting whether to overwrite or append table

        """

        # create 
        df = pd.read_csv(filename)

        # determine if numpy or python type and convert accordingly
        types = []
        for item in df.iloc[0]:
            if type(item).__module__ == 'numpy':
                types.append(type(item.item()))
            else:
                types.append(type(item))

        # create table if necessary
        if not self.engine.has_table(table):
            self.create_table(table, df.columns, types)

        try:
            if overwrite:
                df.to_sql(table, self.engine, if_exists='replace', index=False)
            else:
                df.to_sql(table, self.engine, if_exists='append', index=False)
        except ValueError as e:
            print(e)
            quit() 

    def insert_directory(self, directory, table, overwrite):
        """Insert all csv files from directory into table.

        Args:
            directory (string): directory to insert
            table (string): table to insert into
            overwrite (bool): If true, overwrite table in sql database. If false, append.
        """

        # iterate over filenames and insert CSVs as found
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                path = os.path.join(directory, filename)
                self.insert_from_CSV(path, table, overwrite)

                # reassign overwrite so that insert_from_CSV doesn't overwrite on each insert
                overwrite = False

    def create_table(self, table, columns, types):
        """ create table from given dataframe

            args:
                table ---- name of table to be created
                columns ---- list of column names
                types ---- list of types for the columns
        """
        
        # create table with dataframe data
        sql_table = alc.Table(
            table, self.meta,
            alc.Column('id', alc.Integer, primary_key=True),
            *(alc.Column(column_name, self.type_dict[column_type]) for column_name, column_type in zip(columns, types)))

        # create table in database
        self.meta.create_all(self.engine)

    def select(self, query_tables, conditions={}, pandas=False):
        """ Select elements with corresponding row and column values

            args:
                query_tables ---- list of tables to select elements from

            kwargs:
                conditions ---- dictionary of column names and conditions.
                                conditions are represented as a three-tuple of 
                                table, operation and operand value.
                pandas ---- If true, return dataframe. If false, return resultproxy.
            
            example: Session.select(['test'], {'id': ('test', '>', '1')})
            
        """

        # create table objects out of table names
        self.meta.reflect(self.engine)
        tables = []
        for table in query_tables:
            tables.append(self.meta.tables[table])

        # create query in specified tables
        query = alc.sql.select(tables)
        
        # add condition for each column to select
        for column in conditions:
            query = query.where(comp_string_to_op(conditions[column][1])(self.meta.tables[conditions[column][0]].columns[column], conditions[column][2]))

        # return results
        if pandas:
            return pd.read_sql(str(query), self.conn)
        else:
            return self.conn.execute(query).fetchall()

    def rename_table(self, old, new):
        """Rename an existing table in the database
        """
        self.conn.execute(alc.sql.text('ALTER TABLE ' + old + ' RENAME TO ' + new))
    

def comp_string_to_op(string):
    """ Converts string of expression to sqlalchemy binaryexpression
    """

    ops = {
        '>' : operator.gt,
        '>=' : operator.ge,
        '<' : operator.lt,
        '<=' : operator.le,
        '==' : operator.eq,
        '!=' : operator.ne
    }

    return ops[string]