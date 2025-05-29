release: python manage.py migrate --no-input && python manage.py collectstatic --noinput
web: gunicorn wafa.wsgi --timeout 60 --keep-alive 5 --log-level info
