# buchelly-api

## Linux requirements
- python 3.10.12
- pip 22.0.2


## Clone the repository

`git clone git@github.com:Mici7120/buchelly-api.git`

`cd buchelly-api`

## Install venv for virtual enviroments

`sudo apt install python3.10-venv`

## Create the virtual enviroments

`python3 -m venv venv`

## Activate the virtual enviroment

`source venv/bin/activate`

## Install the requirements

`pip install -r requirements.txt`

## Make migrations

`python manage.py makemigrations`

## Run Migrations

`python manage.py migrate`

# Run Server

`python manage.py runserver`

## Update the requirements

`pip freeze > requirements.txt`
