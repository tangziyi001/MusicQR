First installation:
$ ./first_install.sh

Install mysql-server
$ sudo apt-get update; sudo apt-get install mysql-server
(Set a mysql root password)

Install the proper databases
$ cd db
$ ./install_db.sh
(Will ask for the mysql root password configured above).
$ cd ..

Sync the database
$ cd env
$ source ./bin/activate
$ cd web/scalica
$ python manage.py migrate


# After the first installation, from the project's directory
Run the server:
$ cd env
$ source ./bin/activate
$ cd web/scalica
$ python manage.py runserver

Access the site at http://localhost:8000/micro
