My Live Notebook
================

A Basic Python project built with flask web framework 

Flask
=====
Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. It began as a simple wrapper around Werkzeug and Jinja and has become one of the most popular Python web application frameworks.
It even contains security for login process and include functionality for fetching data from remote server

The Project also shows how to fetch/scrap data from remote sites using APIs and basic tools(scrapying data from html pages)


Install & Setup
===============

Create a virtualenv and activate it::

    $ python3 -m venv venv
    $ . venv/bin/activate

Or on Windows cmd::

    $ py -3 -m venv venv
    $ venv\Scripts\activate.bat

Add a db file for sqlite3 database under::

    $ C:\sqlite3\test.db

To Install all dependencies

    $ pip install -r requirements.txt

Run
---
(..navigate for project folder in the terminal)
on Linux terminal::

    $ export FLASK_APP=flaskr
    $ export FLASK_ENV=development
    $ flask init-db
    $ flask run

Or on Windows cmd::

    > set FLASK_APP=main.py
    > set FLASK_ENV=development
    > flask run

Open http://127.0.0.1:5000 in a browser.

