JDBC Connection for SQLAlchemy.
===============================
.. image:: https://img.shields.io/pypi/dm/sqlalchemy-jdbcapi.svg
        :target: https://pypi.org/project/sqlalchemy-jdbcapi/

The primary purpose of this dialect is provide JDBC connection using required driver.

Installation
------------

Installing the dialect is straightforward::

     python3 -m pip install sqlalchemy-jdbcapi


Usage
-----

PostgressSQL::

    Set an environment variable  `PG_JDBC_DRIVER_PATH`
    from sqlalchemy import create_engine
    create_engine('jdbcapi+pgjdbc://{}:{}@{}/{}'.format(username, password, <ip:host>', <database name>))

Oracle::

    Set an environment variable `ORACLE_JDBC_DRIVER_PATH`
    create_engine("jdbcapi+oraclejdbc://username:password@HOST:1521/Database")

GenericJDBCConnection::

        Set an environment variable `JDBC_DRIVER_PATH`

Supported databases
-------------------

In theory every database with a suitable JDBC driver should work.

* SQLite
* Hypersonic SQL (HSQLDB)
* IBM DB2
* IBM DB2 for mainframes
* Oracle
* Teradata DB
* Netezza
* Mimer DB
* Microsoft SQL Server
* MySQL
* PostgreSQL
* many more...

Contributing
------------

Please submit `bugs and patches
<https://github.com/daneshpatel/sqlalchemy-jdbcapi/issues>`_.
All contributors will be acknowledged. Thanks!

Changelog
------------
- 1.1.0 - 2020-08-4
  - Initial release.