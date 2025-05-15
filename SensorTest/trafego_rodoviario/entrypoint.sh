#!/bin/sh
if [ "$MIGRATE" == "True" ]; then
    python manage.py migrate -v 3
elif [ "$MIGRATIONS" == "True" ]; then
    python manage.py makemigrations -v 3
elif [ "$SHELL" == "True" ]; then
    python manage.py shell_plus  --ipython
else
    python manage.py runserver 0.0.0.0:8000
fi