# Server Configuration for Django Project: Tienda

## Overview
This document outlines the server setup for deploying the Django project "Tienda" using Gunicorn and Nginx on an Ubuntu server hosted on AWS EC2.

### Server Details
- **Operating System**: Ubuntu 20.04 LTS
- **Python Version**: 3.12.6
- **Database**: PostgreSQL 13
- **Web Server**: Nginx
- **Application Server**: Gunicorn
- **Environment**: AWS EC2 Instance
- **Project Location**: `/home/ubuntu/tienda`
- **Virtual Environment**: `/home/ubuntu/venv`

---

## Steps to Set Up the Server

### 1. **Initial Server Setup**
- Update and upgrade the server:

    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

- Install necessary system dependencies:

    ```bash
    sudo apt install -y python3-pip python3-venv nginx libjpeg-dev zlib1g-dev \
        libtiff-dev libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev \
        libfribidi-dev tcl-dev tk-dev postgresql postgresql-contrib
    ```

### 2. **Set Up PostgreSQL Database**
- Create a PostgreSQL database and user:

    ```sql
    sudo -u postgres psql
    CREATE DATABASE tienda;
    CREATE USER tienda_user WITH PASSWORD 'your_password';
    ALTER ROLE tienda_user SET client_encoding TO 'utf8';
    ALTER ROLE tienda_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE tienda_user SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE tienda TO tienda_user;
    \q
    ```

### 3. **Set Up the Python Virtual Environment**
- Create and activate the virtual environment in `/home/ubuntu/venv`:

    ```bash
    python3 -m venv /home/ubuntu/venv
    source /home/ubuntu/venv/bin/activate
    ```

- Install project dependencies:

    ```bash
    pip install --upgrade pip
    pip install -r /home/ubuntu/tienda/requirements.txt
    ```

### 4. **Set Up Gunicorn**
- Install Gunicorn:

    ```bash
    pip install gunicorn
    ```

- Create a systemd service file for Gunicorn at `/etc/systemd/system/gunicorn.service`:

    ```ini
    [Unit]
    Description=gunicorn daemon for Django project
    After=network.target

    [Service]
    User=ubuntu
    Group=www-data
    WorkingDirectory=/home/ubuntu/tienda
    ExecStart=/home/ubuntu/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/tienda/tienda.sock tienda.wsgi:application

    [Install]
    WantedBy=multi-user.target
    ```

- Reload systemd and start Gunicorn:

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn
    ```

### 5. **Set Up Nginx**
- Create an Nginx configuration file at `/etc/nginx/sites-available/tienda`:

    ```nginx
    server {
        listen 80;
        server_name your_domain_or_IP_publica;

        location / {
            include proxy_params;
            proxy_pass http://unix:/home/ubuntu/tienda/tienda.sock;
        }

        location /static/ {
            alias /home/ubuntu/tienda/static/;
        }

        location /media/ {
            alias /home/ubuntu/tienda/media/;
        }

        error_log /var/log/nginx/error.log;
        access_log /var/log/nginx/access.log;
    }
    ```

- Enable the Nginx site and restart the service:

    ```bash
    sudo ln -s /etc/nginx/sites-available/tienda /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

### 6. **Permissions**
- Ensure the Nginx user has the necessary permissions to access the project directory:

    ```bash
    sudo chmod o+rx /home/ubuntu
    ```

### 7. **Firewall Configuration**
- Allow HTTP and HTTPS traffic through the firewall:

    ```bash
    sudo ufw allow 'Nginx Full'
    ```

### 8. **Testing and Deployment**
- Verify the application is accessible via the domain or public IP.

---

## Troubleshooting

### Gunicorn Not Starting
- Check the status of Gunicorn:

    ```bash
    sudo systemctl status gunicorn
    ```

- View Gunicorn logs:

    ```bash
    sudo journalctl -u gunicorn
    ```

### Nginx 502 Bad Gateway
- Ensure Gunicorn is running and the socket exists:

    ```bash
    sudo systemctl status gunicorn
    ls /home/ubuntu/tienda/tienda.sock
    ```

- Check Nginx logs:

    ```bash
    sudo tail -f /var/log/nginx/error.log
    ```

---

## Future Improvements
- Add SSL certificates using Let's Encrypt:

    ```bash
    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d your_domain
    ```

- Automate deployments using CI/CD pipelines (e.g., GitHub Actions).

