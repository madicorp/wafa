release: ./manage.py migrate --no-input
web: gunicorn wafa.wsgi --timeout 60 --keep-alive 5 --log-level debug
