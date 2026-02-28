web: python3 manage.py migrate && python3 manage.py seed_data && python3 manage.py collectstatic --noinput && gunicorn iluffy_landingpage.wsgi --bind 0.0.0.0:$PORT
