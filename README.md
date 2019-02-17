# Leawood-MW
The middleware component for the Leawood project - based on Test Driven Development

## Setting up
```
# Download and unzip the Leawood-MW repository

cd leawood-MW

# If the geckodriver is not in the path (i.e. Windows), download it and install 
# it in the Leawood-MW directory.

virtualenv -p python3.6 virtualenv
. ./virtualenv/bin/activate
pip install django selenium

python manage.py runserver

python function_test.py

```
