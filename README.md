nwk_mall
========
Shopping mall application back end

Installation
===========
First, you must have a mysql server running. 

Change root password to root:
	mysqladmin -u root password root

To run mysql server:
	mysqld

Then, create a new database:
	mysql -uroot -p root -e "CREATE DATABASE IF NOT EXISTS shopgrab_db;"

Use pip to install all dependencies
	pip install -r requirements.txt

Migrate django database
	cd ./backend
	python manage.py migrate

Finally, run the server
	python manage.py runserver

Note: Docker will be supported in near future