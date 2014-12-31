nwk_mall
========
Shopping mall application back end

Installation
===========
First, you must install mysql server 

```
# Change root password to root:
mysqladmin -u root password root

#To run mysql server:
mysqld

#Then, create a new database:
mysql -uroot -p root -e "CREATE DATABASE IF NOT EXISTS shopgrab_db;"

#Use pip to install all dependencies
pip install -r requirements.txt

#Migrate django database
cd ./backend
python manage.py migrate

#Finally, run the server
python manage.py runserver 0.0.0.0:8000
```

Note: Docker will be supported in near future

Fake Data
=========
To insert fake data to the database
```
python manage.py fake_data
```

If you want to remove all data in the database
```
python manage.py flush
```

OAuth2
======
##Application registration
Go to /o/applications/ to register a new application. Take note of the client_id and client_secret.

```
Client type: confidential
Grant type: Resource-owned password based
```

##Getting access token
Follow the convention specified in the test_oauth_consumer.py file for requesting access token.

Need to send:
* grant_type
* username
* password
* client_id of application
* client_secret of application

##API Usage
Add this in the request header of API:
```
Authorization: Bearer *access_token*
```