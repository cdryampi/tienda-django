# Tienda - Proyecto Django

Este es un proyecto basado en Django 5.0 que implementa una tienda en línea con funcionalidades como:

- Autenticación de usuarios con django-allauth y login social.
- Carrito de compras con django-money para múltiples monedas.
- Pagos con Stripe (¡sí, ahora puedes cobrar!).
- Soporte multi-idioma con django-parler.
- Pipeline de despliegue a AWS (posiblemente eliminada antes de que me cobren 💸).
- Frontend experimental con Vue.js a través de django-vite.

## 💡 **Disclaimer**: Este proyecto ya estaba avanzado antes de integrar Stripe, pero se realizaron adaptaciones para que los pagos funcionaran sin romper todo (o casi).

## Índice

1. 🛠 [Requisitos previos](#-requisitos-previos)
2. 🚀 [Instalación](#-instalación)
3. 🛒 [Integración con Stripe](#-integración-con-stripe)
4. 📂 [Aplicaciones Instaladas](#aplicaciones-instaladas)
5. 🔐 [Autenticación y Permisos](#-autenticación-y-permisos)
6. 🌍 [Configuración de Idiomas](#-configuración-de-idiomas)
7. 📦 [Archivos Estáticos y Multimedia](#-archivos-estáticos-y-multimedia)
8. 💼 [Panel de Administración](#-panel-de-administración)
9. 🚢 [Despliegue en Producción](#-despliegue-en-producción)
10. 📝 [Historias de Guerra](#retos-y-problemas-encontrados)

---

## 🛠 Requisitos previos

Antes de empezar, asegúrate de tener:

- Python 3.12+ 🐍
- PostgreSQL 🐘
- Virtualenv (opcional, pero recomendado)
- Node.js (opcional, si quieres probar la UI con Vue.js)

---

## 🚀 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/tienda.git
cd tienda
```

2. Crear y activar un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias **Importante: instalar getText**:

```bash
pip install -r requirements.txt
```

4. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```bash
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

5. Crea la base de datos y ejecuta las migraciones:

```bash
python manage.py migrate
```

6. Carga los datos iniciales:

```bash
python manage.py create_initial_data
```

7. Crea un superusuario:

```bash
python manage.py runserver
```

---

## 🛒 Integración con Stripe

Este proyecto usa Stripe en la app `payments` para procesar pagos de manera segura.

- Gestiona y procesa los pagos de los carritos de compra de los usuarios y de los usuarios sin cuenta.
- Webhooks de Stripe actualizan el estado de pago en la base de datos.
- Se almacenan facturas y enlaces de recibo en cada orden.

---

### Tarjetas de Prueba

| Tarjeta             | Estado                  |
| ------------------- | ----------------------- |
| 4242 4242 4242 4242 | Pago exitoso            |
| 4000 0000 0000 9995 | Pago rechazado          |
| 4000 0025 0000 3155 | Autenticación requerida |

---

### Demostración del funcionamiento de Stripe en la tienda

1. Añade productos al carrito.
   ![Carrito de compras](docs/images/carrito_con_productos.png)

   1.1 **Nota**: Si no tienens cuenta, lo guardarás en la sesión.

   1.2 **Importante**: No te dejará pagar si no tienes productos en el carrito.

2. Vez a la página de pago.
   ![/cart/detail/](docs/images/pagina_de_pago.png)
   2.1 **Nota**: Podemos modificar la cantidad de productos en el carrito de forma reactiva gracias a Vue.js.
3. Procede al pago.
   ![Página de pago](docs/images/pagina_de_pago_2.png)
   3.1 **Nota**: Dejamos que el Stripe gestione la autenticación y el pago. No almacenamos datos de tarjetas, ni datos del cliente. Solo los datos que Stripe nos devuelve.
4. Completa el pago con una tarjeta de prueba.
   ![Pago completado](docs/images/pago_procesando.png)
   4.1 **Nota**: Stripe nos devuelve un `payment_intent` que almacenamos en la base de datos para futuras referencias.
5. Copia el identificador de la orden y ve a la página de detalles.
   ![Orden completada](docs/images/orden_completada.png)
   5.1 **Nota**: Podemos ver los detalles de la orden. Si el pago falla, se mostrará un mensaje de error.
6. Revisa los detalles de la orden en el buscador de facturas `buscar factura`.
   ![Detalles de la orden](docs/images/detalles_de_la_orden.png)
   6.1 **Nota**: Podemos ver los detalles de la orden, la factura.
7. Al no tener un cuenta configurada, Stripe no nos devolverá de forma automática la factura. Pero podemos recuperarla desde el dashboard de Stripe.
   ![Dashboard de Stripe](docs/images/dashboard_stripe.png)
   7.1 **Nota**: Podemos ver las facturas, los pagos y los detalles de la orden en el dashboard de Stripe.

---

## Aplicaciones Instaladas

- `accounts`: Autenticación de usuarios con django-allauth.
- `cart`: Carrito de compras con django-money.
- `core`: Configuración de la tienda y modelos genéricos.
- `orders`: Procesamiento de órdenes y pagos con Stripe.
- `payments`: Integración con Stripe y webhooks.
- `products`: Catálogo de productos y categorías.
- `translations`: Soporte multi-idioma con django-parler.
- `vitefront`: Frontend experimental con Vue.js y django-vite.

---

## 🔐 Autenticación y Permisos

La autenticación de usuarios se realiza con django-allauth, que permite a los usuarios registrarse con su correo electrónico, nombre de usuario o a través de redes sociales como Facebook.

- Login con usuario y contraseña.
- Permisos de usuario, superusuario y staff.

```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
]
```

---

## 🌍 Configuración de Idiomas

El proyecto soporta múltiples lenguajes con django-parler, que permite traducir los modelos y las vistas de la tienda.
**Nota**: Asegúrate de tener gettext instalado en tu sistema. La tienda solo tiene traducido los productos para probar el `django-money` y ver cómo los precios cambian de acuerdo al idioma.

```python
LANGUAGES = [
    ('es', 'Español'),
    ('en', 'Inglés'),
    ('fr', 'Francés'),
]
```

---

## 📦 Archivos Estáticos y Multimedia

El proyecto utiliza una app independiente para almacenar los archivos estáticos y multimedia. Además de comprimir los archivos estáticos con `imagekit`.

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

---

## 💼 Panel de Administración

El panel de administración de Django se ha personalizado para mostrar los modelos de la tienda de forma más amigable y con más funcionalidades.

- Personalización de los modelos de la tienda.
- Filtros y búsquedas avanzadas.
- Restricciones de visualización a los usuarios staff.

```python
JAZZMIN_SETTINGS = {
    "site_title": "Admin de Mi Tienda",
    "site_header": "Mi Tienda",
    "site_brand": "Mi Tienda",
    "welcome_sign": "Bienvenido al Panel de Administración",
}
```

---

## Frontend con Vue.js

El proyecto incluye una app que se basa en `django-vite` para compilar y servir archivos de Vue.js en el servidor de desarrollo y compilar los ficheros en producción.

- Integración de Vue.js con Django.
- Gestión de alertas y mensajes con `vue-sonner`
- Componentes de `flowbite`
- Estilos con `tailwindcss`

```python
# Configuración de Vite-Django
# ⚡ Ajustar para producción
DJANGO_VITE = {
    "default": {
        "manifest_path": BASE_DIR / "vitefront" / "dist" / ".vite" / "manifest.json",
    }
}

DJANGO_VITE_ASSETS_PATH = BASE_DIR / "static_files" / "dist"

DJANGO_VITE_DEV_MODE = False  # Modo desarrollo o producción
DJANGO_VITE_DEV_SERVER_URL = "http://localhost:5173"  # Servidor de desarrollo de Vite
```

---

## 🚢 Despliegue en Producción

El proyecto incluye un pipeline de despliegue a AWS con GitHub Actions. **Nota**: Asegúrate de tener configurado tu entorno de producción antes de desplegar.

- Despliegue automático a AWS.
- Configuración de variables de entorno.

```yaml
name: Django CI/CD

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_USER: ${{ secrets.POSTGRES_USER }}
          POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}
          POSTGRES_DB: ${{ secrets.POSTGRES_DB }}
          SECRET_KEY: ${{ secrets.DJANGO_SECRET_KEY }}
        ports:
          - 5432:5432
        options: >-
          --health-cmd="pg_isready -U postgres"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.12.6"

      - name: Install system dependencies for Pillow
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            libjpeg-dev \
            zlib1g-dev \
            libtiff-dev \
            libfreetype6-dev \
            liblcms2-dev \
            libwebp-dev \
            libharfbuzz-dev \
            libfribidi-dev \
            tcl-dev \
            tk-dev

      - name: Install getText
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            gettext

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Wait for PostgreSQL
        run: until pg_isready -h localhost -p 5432 -U ${{ secrets.POSTGRES_USER }}; do sleep 1; done

      - name: Run Django tests
        env:
          DJANGO_SETTINGS_MODULE: tienda.settings
          POSTGRES_DB: ${{ secrets.POSTGRES_DB }}
          POSTGRES_USER: ${{ secrets.POSTGRES_USER }}
          POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}
          DJANGO_SECRET_KEY: ${{ secrets.DJANGO_SECRET_KEY }}

        run: |
          python manage.py migrate

      - name: Create initial data
        run: python manage.py create_initial_data

  deploy:
    runs-on: ubuntu-latest
    needs: test # Asegura que el job de test pase antes de hacer el deploy

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Install SSH key
        uses: webfactory/ssh-agent@v0.5.3
        with:
          ssh-private-key: ${{ secrets.AWS_SSH_PRIVATE_KEY }}

      - name: Prepare permissions before pull and delete .env file and static files
        run: |
          ssh -o StrictHostKeyChecking=no ubuntu@${{ secrets.AWS_EC2_HOST }} << 'EOF'
            sudo chown -R ubuntu:www-data /home/ubuntu/tienda-django/media/
            sudo chmod -R 775 /home/ubuntu/tienda-django/media/
            sudo rm -f /home/ubuntu/tienda-django/.env
            sudo rm -r /home/ubuntu/tienda-django/static_files/
            sudo mkdir /home/ubuntu/tienda-django/static_files/
            sudo chown -R ubuntu:www-data /home/ubuntu/tienda-django/static_files/
            sudo chmod -R 775 /home/ubuntu/tienda-django/static_files/
          EOF
      - name: Generate .env file on the server
        run: |
          ssh -o StrictHostKeyChecking=no ubuntu@${{ secrets.AWS_EC2_HOST }} << 'EOF'
            echo "DJANGO_SECRET_KEY=${{ secrets.DJANGO_SECRET_KEY }}" > /home/ubuntu/tienda-django/.env
            echo "ALLOWED_HOSTS=${{ secrets.ALLOWED_HOSTS }}" >> /home/ubuntu/tienda-django/.env
            echo "POSTGRES_DB=${{ secrets.POSTGRES_DB }}" >> /home/ubuntu/tienda-django/.env
            echo "POSTGRES_USER=${{ secrets.POSTGRES_USER }}" >> /home/ubuntu/tienda-django/.env
            echo "POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }}" >> /home/ubuntu/tienda-django/.env
            echo "FACEBOOK_APP_ID=${{ secrets.FACEBOOK_APP_ID }}" >> /home/ubuntu/tienda-django/.env
            echo "FACEBOOK_APP_SECRET=${{ secrets.FACEBOOK_APP_SECRET }}" >> /home/ubuntu/tienda-django/.env
            echo "STRIPE_PUBLIC_KEY=${{ secrets.STRIPE_PUBLIC_KEY }}" >> /home/ubuntu/tienda-django/.env
            echo "STRIPE_SECRET_KEY=${{ secrets.STRIPE_SECRET_KEY }}" >> /home/ubuntu/tienda-django/.env
            echo "DEBUG=${{ secrets.DEBUG }}" >> /home/ubuntu/tienda-django/.env
          EOF

      - name: Deploy to EC2
        run: |
          ssh -o StrictHostKeyChecking=no ubuntu@${{ secrets.AWS_EC2_HOST }} << 'EOF'

            # Matar cualquier proceso de npm que esté corriendo
            cd /home/ubuntu/tienda-django
            git pull origin main
            source /home/ubuntu/venv/bin/activate
            pip install -r requirements.txt
            python manage.py compilemessages
            python manage.py migrate

            # Construcción de Vite (sin npm run dev)
            cd vitefront
            npm install
            npm run build
            cd ..

            # Copiar archivos estáticos de Vite a Django
            python manage.py collectstatic --noinput --clear
            python manage.py create_initial_data

          EOF

      - name: Restore permissions after pull and restart Gunicorn
        run: |
          ssh -o StrictHostKeyChecking=no ubuntu@${{ secrets.AWS_EC2_HOST }} << 'EOF'
            sudo chown -R www-data:www-data /home/ubuntu/tienda-django/media/
            sudo chown -R www-data:www-data /home/ubuntu/tienda-django/static_files/
            sudo chmod -R 775 /home/ubuntu/tienda-django/media/
            sudo chmod -R 775 /home/ubuntu/tienda-django/static_files/
            sudo chmod +x /home/ubuntu/tienda-django/scripts/reiniciar.sh
            cd /home/ubuntu/tienda-django/scripts
            ./reiniciar.sh
          EOF
```

- **Nota**: Se esta valorando hacer un force al pull para evitar conflictos en el despliegue.

---

## Retos y problemas encontrados

En el desarrollo de este proyecto, me encontré con varios problemas y retos que tuve que resolver. Algunos de ellos fueron:

- Bugs del parler, al migrar hay que tener cuidado con las migraciones.
- bugs con el vitefront, al compilar los archivos de Vue.js.
- Problemas con la pipeline de despliegue, al no devolver mensajes de logs claros.
- Problemas con la configuración de las variables de entorno, al no tener un archivo `.env` en producción.
- Problemas con la configuración de los webhooks de Stripe, al no recibir las notificaciones de pago.
- Problemas de CORS con el frontend de Vue.js, al no poder acceder a los datos de la API.
- Problemas con el Django-guardian, al no poder asignar permisos a los usuarios.
- Casi todos los problemas se resolvieron a base de scripts para gestionar los datos y liberar de modificar manualmente las migraciones que genera django y evitar realizar pasos exóticos que comprometan la integridad de los datos.
