## Run in Develop
Create new venv
```
python -m virtualenv myboardenv
```

Run env
```
(Windows) source myboardenv/Scripts/activate
(MacOS) source myboardenv/bin/activate
```

Install library
```
pip install -r requirements.txt
```

Migrate Database
```
python manage.py migrate
```

Create superuser
```
python manage.py createsuperuser
```

Run
```
(Windows)  winpty python manage.py createsuperuser
(MacOS) python manage.py runserver
```

## Note
Stop mysqld
```
net stop MySQL80
```

Create new app
```
django-admin startapp app_name
```

Run Migration
```
python manage.py makemigrations app_name
python manage.py migrate app_name
```