# Tienda - Proyecto Django

Este es un proyecto basado en Django 5.0 que implementa una tienda en línea con funcionalidades como autenticación de usuarios, carrito de compras, pagos y soporte para múltiples idiomas.

## Requisitos previos

Asegúrate de tener instalados los siguientes requisitos antes de continuar:

- Python 3.12+
- PostgreSQL
- Virtualenv
- Node.js (opcional, si usas JavaScript para la UI)
- Un archivo `.env` con las configuraciones necesarias

## Instalación

1. Clonar el repositorio:
   ```sh
   git clone https://github.com/tu_usuario/tienda.git
   cd tienda
   ```

2. Crear y activar un entorno virtual:
   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```sh
   pip install -r requirements.txt
   ```

4. Configurar el archivo `.env` con tus credenciales:
   ```ini
   SECRET_KEY=tu_secreto
   DATABASE_NAME=tienda
   DATABASE_USER=tienda
   DATABASE_PASSWORD=thos
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   STRIPE_PUBLIC_KEY=tu_clave_publica
   STRIPE_SECRET_KEY=tu_clave_secreta
   FACEBOOK_APP_ID=tu_facebook_id
   FACEBOOK_APP_SECRET=tu_facebook_secret
   ```

5. Aplicar migraciones:
   ```sh
   python manage.py migrate
   ```

6. Generar los datos iniciales:
   ```sh
   python manage.py create_initial_data
   ```

7. Ejecutar el servidor:
   ```sh
   python manage.py runserver
   ```

## Configuración de la base de datos

Este proyecto utiliza PostgreSQL como base de datos. Configuración en `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tienda',
        'USER': 'tienda',
        'PASSWORD': 'thos',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Aplicaciones Instaladas

El proyecto incluye las siguientes aplicaciones:

- `accounts` - Gestión de usuarios y autenticación con `django-allauth`.
- `cart` - Funcionalidad de carrito de compras.
- `payments` - Integración con Stripe.
- `product` - Gestión de productos.
- `multimedia` - Gestión de archivos multimedia.
- `pricing` - Manejo de precios y conversión de divisas.
- `common` - Funcionalidades compartidas.
- `core` - Configuración principal.

## Autenticación y Permisos

Este proyecto usa `django-allauth` y `django-guardian` para autenticación y permisos:

- Se permite el login con email o usuario.
- Se usa `guardian` para permisos a nivel de objeto.

```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
]
```

## Configuración de idiomas

El proyecto soporta múltiples idiomas mediante `django-parler`:

```python
LANGUAGES = [
    ('es', 'Español'),
    ('en', 'Inglés'),
    ('fr', 'Francés'),
]
```

## Archivos estáticos y multimedia

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## Panel de administración

El administrador está personalizado con `django-jazzmin`:

```python
JAZZMIN_SETTINGS = {
    "site_title": "Admin de Mi Tienda",
    "site_header": "Mi Tienda",
    "site_brand": "Mi Tienda",
    "welcome_sign": "Bienvenido al Panel de Administración",
}
```

## Despliegue en producción

1. Cambiar `DEBUG = False` en `settings.py`.
2. Configurar `ALLOWED_HOSTS` correctamente.
3. Ejecutar `collectstatic`:
   ```sh
   python manage.py collectstatic
   ```
4. Configurar Gunicorn y Nginx para servir la aplicación.