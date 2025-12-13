echo "Migrating database..."
python -m manage migrate

echo "Collecting static files..."
python -m manage collectstatic --noinput
