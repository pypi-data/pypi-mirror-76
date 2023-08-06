djfirebirdsql
==============

Django Microsoft SQL Server backend.

I refer to djang-pyodbc-azure (https://github.com/michiya/django-pyodbc-azure).

Requirements
-------------

* Django 3.1
* minitds (https://github.com/nakagami/minitds) recently released.

Installation
--------------

::

    $ pip install djmssql django

Database settings example
------------------------------

::

    DATABASES = {
        'default': {
            'ENGINE': 'djmssql',
            'NAME': ...,
            'HOST': ...,
            'USER': ...,
            'PASSWORD': ...,
        }
    }
