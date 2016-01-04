Dynamic models
==============

Django application that allows you to dynamically create a table in the database

Based on [dynamo](https://bitbucket.org/mhall119/dynamo/)

The sample application comes with:

```
"jquery": "2.1.1",
"angular": "1.2.x",
"angular-mocks": "~1.2.x",
"angular-route": "~1.2.x",
"angular-resource": "~1.2.x",
"underscore": "1.6.0",
"bootstrap": "3.2.0",
"bootstrap-growl": "~2.0.1",
"modernizr": "2.8.3",
"font-awesome": "4.1.0",
"animate.css": "3.2.0"
```

And its current `requirements.txt` file is:

```
Django==1.7
argparse==1.2.1
django-appconf==0.6
django-compressor==1.4
djangorestframework==2.4.2
psycopg2==2.5.4
six==1.8.0
wsgiref==0.1.2
```

## Installation

### download

    $ git clone https://github.com/rendrom/django-dynamit.git
    $ cd ./django-dynamit
    
### virtualenv

    $ virtualenv --distribute ./.env
    $ . ./.env/bin/activate
    
### Requirements

    $ pip install -r ./requirements.txt
    
### Install the frontend code

To setup and run the sample code, you're going to need `npm` from NodeJS available to install the frontend code.

    $ npm install -g grunt-cli bower
    $ npm install
    $ bower install
    
### Local Settings

Create `local_settings.py` and modify necessary changes

    $ cp ./prj/local_settings.py.template ./prj/local_settings.py
    
### Initialize the database

    $ ./manage.py migrate
    $ make superuser
    
### Run the Server

    $ ./manage.py runserver
    
## Demonstration

* Demo server - [http://geonote.ru](http://geonote.ru)
* Video - [http://youtu.be/uwjknqwZDqE?list=UUXcVKbtnzWyuejxvuvLndZg](http://youtu.be/uwjknqwZDqE?list=UUXcVKbtnzWyuejxvuvLndZg)
