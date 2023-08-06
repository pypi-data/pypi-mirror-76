# CSSAW_Central

## Installation
``` Bash
pip install cssaw-central
```

## Usage

### csvsql script

The package comes with a script to automatically upload a csv file to the given table in a sql database. It takes user, pass, host IP, database, table, and cSV file path as arguments

#### csvsql -h

``` Console
    usage: csvsql [-h] user password host database table filename

    positional arguments:
        user         user for database login
        password     password for login if necessary
        host         host IP for database
        database     database to run queries on
        table        table to insert into (will create new if doesn't exist)
        filename     filepath of CSV file to insert

    optional arguments:
        -h, --help   show this help message and exit
        --overwrite  Overwrite already-present table in database
```

#### example
``` Bash
csvsql test test HOST Test test_table ./TestDocs/test.csv
```

The above example connects to the Test database using the test user and inserts the test.csv file into test_table.

### Session module
Session object acts as a wrapper for sqlalchemy connection. The connection is created and stored in the Session object at initialization, and any results can be taken from the self.conn object or, if using execute_sql(), can be taken from the returned results python list.

#### Example:
```Python
from cssaw_central.Session import Session

sess = Session('username','password', 'localhost', db='Test')

sess.create_table('test_table', ['column1', 'column2', 'column3'], \ 
                    [int, int, int])

sess.insert('test_table', ['column1', 'column2', 'column3'], [0, 1, 2])
print(sess.execute_SQL('./queries/test.sql'))
```

The above script will create a connection to the Test database at localhost:3306 (assuming that it exists), insert the given values into their appropriate columns in test_table, and then execute test.sql from the queries file.

# License
[MPL-2.0](https://opensource.org/licenses/MPL-2.0)
