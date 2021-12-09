## Run in Develop
Create new venv
```
python -m virtualenv myboardenv
```

Run env
```
source myboardenv/Scripts/activate
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
python manage.py runserver
```
