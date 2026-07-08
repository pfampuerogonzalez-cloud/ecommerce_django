#!/usr/bin/env bash
set -o errexit

echo "=== Instalando dependencias ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Migrando base de datos ==="
python manage.py migrate --noinput

echo "=== Creando superusuario por defecto (si no existe) ==="
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superusuario admin creado')
else:
    print('Superusuario ya existe')
"

echo "=== Recolectando archivos estáticos ==="
python manage.py collectstatic --noinput

echo "=== Build completado ==="
