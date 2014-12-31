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
Go to `/admin` to login as administrator. 

If you're using `fake_data`, then you can sign in using:
```
username: admin
password: admin
```

Else you need to create a super user in command line
```
python manage.py createsuperuser
//Then follow the instruction
```

Go to `/o/applications/` to register a new application. Take note of the client_id and client_secret.

```
Name: <Just Give a Name>
Client type: confidential
Grant type: Resource-owned password based
```

If you're using fake_data and debug version of the Android application, then you should also input the following in the `/o/applications/` form
```
Client id : kF0oFIZP7@uiMABQzHLirc8q8hUsz!F!peyUJEV;
Client secret: umK2JXvw?LcDH@KX?5!c8yjBtz-2caNiTLoB6ij6keIYAQEI39UGtv6qaRyuAI8L0wWS9E8!cy!btNxdUIiqZ?1SGcpSv9?jTyjnm;csarQuOpbai3Ccc.th2=G_YVFg
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