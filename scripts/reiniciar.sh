#!/bin/bash

echo "Reiniciando servicios..."

# Reiniciar PostgreSQL
echo "Reiniciando PostgreSQL..."
sudo systemctl restart postgresql

# Reiniciar Gunicorn
echo "Reiniciando Gunicorn..."
sudo systemctl restart gunicorn

# Reiniciar Nginx
echo "Reiniciando Nginx..."
sudo systemctl restart nginx

echo "Todos los servicios han sido reiniciados correctamente."
