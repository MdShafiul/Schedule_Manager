# Schedule_Manager
ERP based web-application in Python using Flask

## Platform:
 Web App

## Requirements:
- Python
- MySQL Server

## Intallation Steps:
 1. __Database Configuration__:

 	Fill up the Schedule_Manager/db.yaml file
 2. __Mail Configuration__:

 	Set __'MAIL_USERNAME'__ and __'MAIL_PASSWORD'__ at 18 , 19 lines of Schedule_Manager/main.py
 3. __Python Packages__:

 	Download python packages
 	```
	pip install -r requirements.txt
	```
 4. __Run App__:

 	To run application locally:
 	```
	python manage.py start
	```
## Visual Representation:
 At first type the url -  http:/localhost:8000 to visit the site. 
 User will see the __'Sign In'__ page of the app. 

![SignIn](screenshots/2_SignIn.png)
  User must have to sign up before

![SignUp](screenshots/1_SignUp.png)
 Profile page 

 __ADD:__ to add a data-table 

 __DELETE:__ to delete a data-table

 Click a project name to view the data-table
![3_Profile](screenshots/3_Profile.png)