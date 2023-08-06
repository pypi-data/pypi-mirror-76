nuvolos - The database connectivity library for Nuvolos
=======================================================

Installation
============

.. code:: bash

    $ pip install nuvolos 

Usage
=====
The library provides two convenience functions for connecting to the remote database with your credentials. There are two possible usage modes. 

1. If you are running python in a Nuvolos application (e.g. JupyterLab), you don't have to provide any arguments or credentials for the library to create a pyodbc connection.
2. If you are running python from a non-Nuvolos application (e.g. your own computer), you have to provide four arguments: your username, your database password, the database and schema of the dataset you want to connect to. This information can be found in the Connection guide in the Nuvolos UI. 

Using in Nuvolos applications
=============================

You can get the ODBC connection string or create a pyodbc connection object:

::

    >>> from nuvolos import get_connection_string, get_connection
    >>> get_connection_string()
    ''DRIVER=SnowflakeDSIIDriver;SERVER=alphacruncher.eu-central-1.snowflakecomputing.com;DATABASE=%22<dbname>%22;SCHEMA=%22<schemaname>%22;UID=<username>;PWD=<password>;CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX=TRUE;VALIDATEDEFAULTPARAMETERS=TRUE
    >>> get_connection_string(username="abc", password="def", dbname="db_name", schemaname="schema_name")
    'DRIVER=SnowflakeDSIIDriver;SERVER=alphacruncher.eu-central-1.snowflakecomputing.com;DATABASE=%22db_name%22;SCHEMA=%22schema_name%22;UID=abc;PWD=def;CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX=TRUE;VALIDATEDEFAULTPARAMETERS=TRUE'
    >>> con = get_connection()

In general, we suggest using :code:`get_connection()` to obtain a pyodbc connection that you can execute statements with.

Using in non-Nuvolos applications
==================================

You can get the ODBC connection string, or pyodbc connection as with Nuvolos, however you will have to provide all four arguments:

::

   >>> from nuvolos import get_connection_string, get_connection
   >>> get_connection_string(username="username", password = "password", dbname = "dbname", schemaname="schemaname")
   'DRIVER=SnowflakeDSIIDriver;SERVER=alphacruncher.eu-central-1.snowflakecomputing.com;DATABASE=%22db_name%22;SCHEMA=%22schema_name%22;UID=abc;PWD=def;CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX=TRUE;VALIDATEDEFAULTPARAMETERS=TRUE'
   >>> con = get_connection(username="username", password = "password", dbname = "dbname", schemaname="schemaname")

You can provide defaults for the above parameters by creating special files.
To avoid typing your username and password directly into your python scripts, you can create a :code:`.odbc.ini` file in your home folder with the following structure:

::

    [nuvolos]
    uid = <username>
    pwd = <password>

To specify the database and schema, you can create a :code:`.dbpath` file in the working directory of your python script
with the contents

::

    "<db_name>"."<schema_name>"
