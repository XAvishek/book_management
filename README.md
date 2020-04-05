# Book Management

Book Management is a web app created using Django and Celery.It can be used to create, update, delete, read books from the web if you are an authenticated user but only view the book if you are an anonymous user

## Installation
Install all the required packages using

pip install -r requirements.txt or pipenv install


### Prerequisites

To work with Celery we need to use a taskbroker.Here I have used RabbitMq.
Install RabbitMQ

For Ubuntu based

```
sudo apt-get install rabbitmq-server
```
For Windows based

```
Download and Install RabbitMq from from www.erlang.org.
```

For Celery 4 to work with Windows you can set thhis variable in your .env file
```
FORKED_BY_MULTIPROCESSING = 1
```


### Getting Started

```
python manage.py migrate
```
After running your first migrate run the command below in a different command promt to run the RABBITMQ server

```
celery -A <project_name> worker -l info
```

And now You can login, signup, from within the browser
and use the code 



## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Celery](http://www.celeryproject.org/) - TaskQueue
* [RabbiMQ](https://www.rabbitmq.com/) - Message Broker 

 

## Authors

* **Avishek Thapa** - *Initial work* - [XAvishek(https://github.com/xavishek)

