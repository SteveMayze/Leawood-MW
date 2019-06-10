# Leawood-MW
The middleware component for the Leawood project - based on Test Driven Development

## Overview
This project is to provide the front end to a set of sensors deployed in the field. The field sensors will transmit their data periodically back to the main system where it is recoreded in a set of database tables. The information is this visible though this front-end.

## Setting up
```
# Download and unzip the Leawood-MW repository

cd leawood-MW

# If the geckodriver is not in the path (i.e. Windows), download it and install 
# it in the Leawood-MW directory.

virtualenv -p python3.6 virtualenv
. ./virtualenv/bin/activate

For Windows, use
. ./virtualenv/Scripts/activate

pip install django selenium

python manage.py collectstatic

python manage.py runserver
```

## Testing
All functional and unit tests can be executed with the following command.
```
python manage.py test

```
