If the populate script fails with "no such table" error, do this:

python manage.py makemigrations
python manage.py migrate
python manage.py migrate --run-syncdb
python populate.py

Should work this way.