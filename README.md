# movies_web_backend
A django powered web page for movies

## Installation
1. Clone the repository
2. Install the requirements
```bash
pip install -r requirements.txt
```
3. Run the server
```bash
python manage.py runserver
```

## Usage
For running tests
```bash
python manage.py test apps.movies.tests
python manage.py test apps.users.tests
```

For creating an admin user
```bash
python manage.py createsuperuser --username admin --email admin@email.com
```
