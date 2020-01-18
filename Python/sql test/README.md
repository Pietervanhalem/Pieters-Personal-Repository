[ ![CircleCI](https://circleci.com/gh/VanOord/sql test.svg?style=shield&circle-token=b74428cc9b75e97046da8db9db84804d8477c7a3)](https://circleci.com/gh/VanOord/sql test)[ ![coverage](https://img.shields.io/badge/code-coverage-blue.svg)](https://circleci.com/api/v1/project/VanOord/sql test/latest/artifacts/0/$CIRCLE_ARTIFACTS/htmlcov/index.html?circle-token=b74428cc9b75e97046da8db9db84804d8477c7a3&branch=master)


# sql test


This template shows a standard way of working with data that comes from files. These files can contain instances of a certain data type.
Such as _\*\*.GEF_ files for CPT's.

# Installation and running sql test

## Installation instructions:

Make sure you have python>3.5.1 and git installed, so they are available from the command line. 

```bash
# clone code from git
git clone https://github.com/VanOord/sql test.git
cd sql test

# upgrade pip
pip install -U pip
pip install -U setuptools

# install requirements
pip install -r requirements.txt

# install this package
pip install -e .
```

Note that, for development, it is advised to manually checkout and install the requirements listed in `requirements-git.txt`.

# Running the app

Make sure that you have a PostgreSQL database server running and an empty database available with the PostGIS extention:

```bash
CREATE EXTENSION postgis;
```

## Database connection

Keep \*.ini files under version control, but **do not store passwords in version control**. Therefore the parameters for the database connection should be defined as environmental variables.

Precedence of the defined parameters for database access is as follows:

1.  sqlalchemy.url set in \*.ini (use this form: `sqlalchemy.url = postgresql://user:password@host:port/dbname`)
2.  `PG_USER`, `PG_PASSWORD`, `PG_HOST`, `PG_PORT` and `PG_DBNAME` set in \*.ini
3.  `PG_USER`, `PG_PASSWORD`, `PG_HOST`, `PG_PORT` and `PG_DBNAME` environmental variables
4.  Default values

(Temporarily) set correct database settings in \*.ini or environmental variables. When using the \*.ini file, make sure **not to commit this file to GitHub**.

The default settings and how to set them as environmental variables are listed below. This differs for windows and linux.

### Linux / OSX

```bash
export PG_PASSWORD=
export PG_USER=postgres
export PG_HOST=localhost
export PG_PORT=5432
export PG_DBNAME=test
```

Add variables to `/etc/environment` to persist them, see [here](https://help.ubuntu.com/community/EnvironmentVariables)

### Windows

```bat
SET PG_PASSWORD=
SET PG_USER=postgres
SET PG_HOST=localhost
SET PG_PORT=5432
SET PG_DBNAME=test
```

Use `SETX` instead to persist the variables, see [here](http://stackoverflow.com/questions/5898131/set-a-persistent-environment-variable-from-cmd-exe)

```bat
SETX PG_PASSWORD
SETX PG_USER postgres
SETX PG_HOST localhost
SETX PG_PORT 5432
SETX PG_DBNAME test
```

Optionally initialize the email SMTP settings:

```bat
SET EMAIL_SMTP_URL=smtp.office365.com:587
SET EMAIL_SMTP_USER=openearth@vanoord.com
SET EMAIL_SMTP_PASSWORD=
```

Again, use `SETX` instead to persist the variables

## Initialize database

When the application is installed (with `pip install ...`), several executable-scripts are made
available on your PATH. This might require a reload of the command prompt / shell environment.
These scripts are made available as executables (.exe on Windows) rather than as python scripts,
so you can run them from anywhere without starting a python instance yourselves (in Anaconda3\Scripts\ on Windows).
With these executable-scripts, the database can be initialised as follows:

    sql_test_initialize_db development.ini

Create fake data to have something to show in the app. This is also done with an executable-script on your PATH.
Make sure that `<outdir>` is equal to the datadirectory set in development.ini.
Note that `sql_test_generate_fake_data` fills and creates this `<outdir>`, so it cannot
be an existing folder.

    pyramid_app_template_generate_fake_data <outdir> <nr cpts> <nr psd files>

And `datadirectory = <outdir>` in development.ini.

Syncronize the database (upload the data):

    pyramid_app_template_sync_db development.ini

Serve with

    pserve development.ini

or for debugging

    pserve development.ini --reload

Browse to `http://localhost:6543`

## Testing

Set environmental variables if necessary (see above) and run

```bash
python setup.py test
```

# run sql_test app in containers

Make sure you have docker and docker-compose installed.

Build the image:

```bash
docker build -t sql_test .
```

Create and run the docker-compose.yml file:

```bash
docker-compose up
```

Start a terminal inside the application container:

```bash
docker exec -it /sql_test_app /bin/bash
```

Install the environment:

```bash
pip install -e .
```

Initialize and synchronize the database:

```bash
sql_test_initialize_db development-docker.ini
sql_test_sync_db development-docker.ini
```

Run the application:

```bash
pserve development-docker.ini --reload
```

Read more about it on the docker-compose [Wiki](../../documentation/wiki/Docker-compose-in-Windows-10).

# Create derivative application

As the new application will be part of the same GitHub account, simply forking the application is not possible. The demo-application can be cloned by following the command line instructions below (after installing SSH keys), or interactively via SourceTree.

Clone this repo and push it to a new repo (that you have to manually create first via the github website): pyramid-app-newrepo:

```
    git clone https://github.com/VanOord/sql test.git pyramid-app-newrepo
    cd pyramid-app-newrepo
    git remote set-url origin https://github.com/VanOord/pyramid-app-newrepo.git
    git remote add upstream https://github.com/VanOord/sql test.git
    git push origin master
    git push --all
```
Note that this only works when `master` is not a protected branch (as you are about to set). 
Don't forget the following steps:

- designate the repository to your team in github
- [build project in CircleCI](https://circleci.com/docs/github-security-ssh-keys/). The current template is by default a ciricle 2.0 project due to the `\.circleci\config.yml`. This makes the test run on a anconda3 docker container.
- set master as a protected branch, with "Require status checks to pass before merging" and subsequently "Include administrators"
- check CircleCI
- create a branch (first had to locally remove and make a new checkout of the sql test and the pyramid-app-newrepo).
- edit the README.md

# App description

This section shortly describes the functionality of the demo application and how to adjust it to your needs.

The application consists of the following components:

* Models: the database model
* Views: makes data from the database viewable in the application
* Template: jade templates for the look of the application
* Tests: all code that is used to test the application
* Scripts: stand alone scripts that can be called independently from the web application from the commandline
* Static: static files that are served as is to clients, typically images, javascript and css.

This template application is built up based on components from the Van Oord pyramid-mod modules. They are described shortly hereafter. For detailed information, read the documentation of the module itself.

### \_\_init__.py
In this configuration file the used models are included. Also the models and the routes are added here.

### routes.py
All the routes in the application are registered here. Details can be found [here](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#route-configuration).

## Models
In the models the database model is defined.

### \_\_init__.py
All model classes are imported here, so that they can easily be accessed via
```python
from sql_test.models import XXX
```
Configurations from modules can be imported in the `includeme` method.

### meta.py
Load sqlalchemy features, no need to edit.

### models.py / models_cpt.py / models_psd.py
All these files contain the discription of the database model. In models.py the actual database tables are defined. The other two files describe instances that are part of the more generic table.

#### Entity
This class is the main class for data entities. This class inherits from:
* The `Base` class from `pyramid_mod_basemodel`: makes it possilble to act with the database
* The `PointMixin` class from `pyramid_mod_geommodel`: makes it possible to deal with geometrical point data.

This class creates the table, the specific entities are added to this table via [Single Table Inheritance](http://docs.sqlalchemy.org/en/latest/orm/inheritance.html#single-table-inheritance)

When using the PointMixin or PolygonMixin here, you need to set the SRID/EPSG of your project.

The `Entity` class has the following **standard** attributes:

* `entity_type` + `mapper_args`: Used later to be able to store different kinds of entities in one table.
* `id`: Unique identifier and primary key
* `name`: Entity\Point name
* `sourcefile_id`: Connection to the sourcefile the data comes from
* `attributes`: Metadata in JSONB (postgres) or dict (python) format
* `data`: Data in JSONB (postgres) or dict (python) format
* `date`: Date data obtained

The `data` and `attributes` columns are kept generic. Easy accessing them can be done with column_properties and is explained below.

For all columns and column_properties the `info` attribute should be added as a dictionary with the keys:

* `displayname`: How to call the attribute in a web page
* `units`: Units of the value (`''` for strings)
* `format`: Way to format the value

#### Sourcefile

This is the main class for source files. This class inherits from:

* The `Base` class from `pyramid_mod_basemodel`: makes it possilble to act with the database
* The `SourceFileMixin` class from `pyramid_mod_basemodel`: standard sourcefile columns

The `sourcefile` class has the following **standard** attributes:

* `file_type` + `mapper_args`: Used later to be able to store different kinds of source files in one table.

This class and classes inheriting from this class always needs to have:

* a `parse` method, as this is used when synchronizing the database to the files
* a variable that makes the `relationship` with the data object from the sourcefile

This example shows a 1:n relationship between source files and entities. More detailed information about the relationship method can be found [here](http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html).

#### CPTs

The CPTs have a 1:1 relation for sourcefile:entity.

#### PSDs

The PSDs have a 1:n relation for sourcefile:entity. Parsing the different enitities to separate table rows is done from the `PsdFile` class.

The use of the `column_property` method is also made clear here. Variables are made for different attributes of the attribute field. These column_properties can be used like any other column in an sqlalchemy query. An explination of the method can be found [here](http://docs.sqlalchemy.org/en/latest/orm/mapped_sql_expr.html#mapper-column-property-sql-expressions)

## Views

Within the views, all the methods that give a response from a URL are defined.

All views are generated with the [`@view_config` decorator](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/viewconfig.html#mapping-views-using-a-decorator-section). The following arguments should be filed in in this order:

* `route_name`: name of the route, use the same name for the method
* `permission`: needed permission for this view
* `renderer`: how to display the response, jade templates can be filled in here

In a standard Van Oord pyramid application with `pyramid_mod_accounts`, the following permissions are available:

* NO_PERMISSION_REQUIRED (from sqlalchemy)
* _client_: access to specific data
* _read_: read-only
* _internal_: access to all data
* _write_: write and edit data
* _superuser_: manage users, add users, soft-delete users
* _admin_: manage users, add users, soft-delete users, permanent-delete users (dangerous)

### \_\_init\_\_.py

The dropdown menu of the application is defined here. For every item, keep the following order:

* `title`: Display title in menu
* `href`: URL to view
* `icon`: Icon (for inspiration, look [here](http://fontawesome.io/icons/))

Also the basic `View` class is defined here.

### home.py / notfound.py / forbidden.py

* home.py: The home page
* notfound.py: When your page couldn't be found
* forbidden.py: When you don't have the correct permissions

### demos.py

The filename of the python file with the views can be everything, so choose a name that suits the views it's generating. The views can also be split over multiple files.

All HTML/Jade views (web-pages) are inherited from View: `class Demos(View):`. The returned dictionary is accessible from the jade templates.

When creating a datatable, use the DataFrameView or QueryView from [`pyramid_mod_dataframe`](https://github.com/VanOord/pyramid-mod-dataframe).

Plots or (geo)jsons are defined outside the `Demo` class. An example of a plot using [Plotly](https://plot.ly/javascript/) is available.

If extra css of javascript is needed within a view, they need to be added to `self.css_requirement_specific` or `self.css_requirement_specific`. Use the `priority` to precisely control the css/js loading order. Priority < 1000 puts them in the header, priority > 1000 puts them in the footer.

#### Plots

For a plot, always return a dictionary with `data` and `layout`.

## Templates

The templates are written in jade. [This is](http://html2jade.org/) good website to help you transform HTML into jade.

All the templates of the application inherit from the main template in `pyramid_mod_baseview`.

```jade
extends pyramid_mod_baseview:templates/main.jade
```

## Scripts

Here the scripts are placed that can be run from outside the application.

In the main `setup.cfg` these scripts can be added as `console_scripts`. This makes them easily accessible from the command line.

```ini
console_scripts =
    sql_test_initialize_db = sql_test.scripts.initializedb:main
```

### initializedb.py

Script that sets up the database based on the application models. The user permissions are added and an admin user.

### syncdb.py

All the data files are synchronized from this script. In this script the `sync_files_to_db` method is used here.

# Rollbar error logging

You can use Rollbar to logg server and client side errors straight to the rollbar service.
Sign up your app in the vanoord account here: https://rollbar.com/VanOord 
Eneable the lines in the `rollbar` options in the *.ini files and enter the access tokens.

# Tests

TO BE ADDED
