Book management system
Book management system is a simple website that gives info to users about the book it's author and languages used in it. This projects allows the authorized user only to create, update and delete the book's info. Here a async message is sent to the author of the book if changes occured in the book

Content
-Installation -Usage

Installation
pip install -r requirements.txt

Usage
In order to use this device first of all,you should install a async task broker such as Redis or RabbitMq.In this project I have used RabbitMq. So, to install RabbitMq for -Ubuntu based System

sudo apt-get install rabbitmq-server

-Windows based System

Please download and Install from RabbitMq website Please install erlang first from www.erlang.org

Then enable and start RabbitMq service for ubuntu based system

systemctl enable rabbitmq-server systemctl start rabbitmq-server

For windows based system please enable the plugin

rabbitmq-plugins enable rabbitmq_management

Then add broker configuration of settings.py file

CELERY_BROKER_URL ='amqp://localhost'

After all the procedure, open a new terminal and run following command

celery -A <project_name> worker -l info NOTE: For those using Windows 10 please write the following code the run the celery task celery -A <project_name> worker -l info -P gevent

The use of dotenv is to store the info of users in environment variable.In order to use it add following code into settings.py. Store your variable in .env file

from dotenv import load_dotenv,find_dotenv load_dotenv()
