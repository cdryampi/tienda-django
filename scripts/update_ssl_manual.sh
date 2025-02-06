#!/bin/bash

echo "🚀 Iniciando actualización manual del certificado SSL..."

# Renovar el certificado con Let's Encrypt (Certbot)
sudo certbot renew --quiet --noninteractive --post-hook "sudo systemctl restart nginx"

echo "✅ Certificado SSL actualizado y Nginx reiniciado."
