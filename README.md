# Final Project for Large Scale Web Application

This is the repository for final project of CSCI-UA480 Large Scale Web Application.

### Configure DB
When the application is run on a new machine, make sure to install mysql and run ./install_db

## Development
* It is recommanded to create a new branch for a specific development task. And then merge the branch with the master. However for convenience, it is ok to push to master directly since there is a backup branch.
* It is recommanded to run local test on Linux machine. Follow the README.txt to setup the environment and tools

## Deployment
* Django Application: ubuntu@35.163.220.222
* Relational Database: tangdb.cyocc9onn55j.us-west-2.rds.amazonaws.com 
* Background Computation and RPC Server: ubuntu@35.163.99.152
* Hadoop Service: ec2-35-161-227-165.us-west-2.compute.amazonaws.com 
## First Install

### Install required packages.
* $ sudo apt-get update; sudo apt-get install mysql-server libmysqlclient-dev python-dev python-virtualenv 
(Set a mysql root password)

* $ ./first_install.sh

### Install the proper databases
* $ cd db
* $ ./install_db.sh (Will ask for the mysql root password configured above).
* $ cd ..

### Sync the database
* $ source ./env/bin/activate
* $ cd web/scalica
* $ python manage.py makemigrations micro
* $ python manage.py migrate

### Setup Backend
* Go to backend/
* $ ./ini.sh
 
### After the first installation, from the project's directory
Run the server:
* $ source ./env/bin/activate
* $ cd web/scalica
* $ python manage.py runserver

Access the site at http://localhost:8000/micro

