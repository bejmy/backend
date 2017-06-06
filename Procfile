release: python manage.py migrate --no-input && python manage.py compilemessages
web: gunicorn bejmy.wsgi
