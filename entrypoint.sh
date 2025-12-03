echo "Starting Entrypoint Script ..."

echo "Apply database migrations ..."
uv run python manage.py migrate

echo "Collect static files  ..."
uv run python manage.py collectstatic --noinput

uv run gunicorn config.wsgi:application --bind 0.0.0.0:8000
