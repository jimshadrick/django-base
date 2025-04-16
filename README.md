# Django Base Project Example

A sample base template that can be used for a new Django project, with support for local development and VPS-based
production deployment.

---

## 🗂 Project Structure

- `project/`: Contains the main Django project configuration.
- `core/`: Contains the core application models and logic.
- `accounts/`: App for user account management and password changes.
- `manage.py`: Django management script for running commands.

---

## ⚙️ Local Development Setup

1. Clone the repository.
2. Install the necessary dependencies using `uv sync`
3. Create and update your `.env` file with the correct database credentials:
    ```env
    DJANGO_DEBUG=True
    DJANGO_SECRET_KEY=supersecretkey
    DATABASE_URL=postgres://postgres:postgres@db:5432/djbasedb
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
    CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
    CONN_MAX_AGE=60
    ```
4. Run migrations and setup:
    ```bash
    uv run manage.py migrate
    uv run manage.py collectstatic
    uv run manage.py createsuperuser
    ```
5. Start the dev server:
    ```bash
    uv run manage.py runserver
    ```

6. Visit `http://localhost:8000/admin` to access the admin panel.

---

## 📦 Package Dependencies

- `django>=5.1.7`
- `environs[django]>=14.1.1`
- `gunicorn>=23.0.0`
- `psycopg[binary]>=3.2.6`
- `whitenoise>=6.9.0`
- `django-allauth[socialaccount]>=65.7.0`

---

### 🔐 Environment Configuration

- `DJANGO_SECRET_KEY`: Secret key for the Django project.
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts.
- `DJANGO_DEBUG`: `True` or `False` (debug mode).
- `DATABASE_URL`: Full connection string for PostgreSQL.
- `CSRF_TRUSTED_ORIGINS`: Comma-separated list of trusted domains.
- `CONN_MAX_AGE`: DB connection max age in seconds (e.g. 60).

---

## 🚀 Production Deployment (DigitalOcean VPS)

This app contains scripts that facilitates deployment to a VPS running Ubuntu, with Gunicorn, Nginx, and systemd.

### 🔧 Prerequisites

- VPS provisioned (e.g., DigitalOcean droplet)
- Non-root user (e.g., `myuser`) configured with sudo access
- SSH access to the VPS
- VPS updated and system packages installed (
  `nginx postgresql postgresql-contrib python3-dev libpq-dev curl build-essential`)
- Python 3.13+ and `uv` installed
- PostgreSQL running and accessible
- Postgres database created and new user created and assigned permissions to database and public schema
- DNS and domain setup (optional)

---

### 📂 Scripts for VPS Deployment

| Script              | Purpose                                                                                                                                                |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `setup_deploy.sh`   | Deploys the app to `/var/www/sites/<project>`, sets ownership, installs Django dependencies, and runs a post-deploy script. Safe to rerun for updates. |
| `create_configs.sh` | One-time system config: creates Gunicorn/Nginx files using `<project_name>`, then enables services and reloads Nginx. Requires `sudo`.                 |
| `post_deploy.sh`    | Called by `setup_deploy.sh`: runs the Django `migrate`, `collectstatic`, and `init_site` commands.                                                     |

---

### 🧪 First-Time Deployment (per app)

```bash
# SSH into your server
ssh myuser@your-server-ip

# Run initial deployment (will create .env if missing)
./setup-deployment.sh myproject

# Test with runserver if desired

# Set up system services
sudo ./create_configs.sh myproject myuser

# Access your app
http://your-domain.com or http://your-server-ip
```

---

### 🔁 Future Deployments (pull latest changes)

```bash
# On the server
./setup_deploy.sh myproject
```

When `setup_deploy.sh` finishes, calls the `post_deploy.sh` which contains these commands:

```bash
uv run python manage.py migrate --noinput
mkdir -p staticfiles
uv run python manage.py collectstatic --noinput```
uv run python manage.py init_site # Django custom command to initialize site (optional) 
```

---

### 🔐 .env Creation Logic

The first deployment will generate a default `.env` like this if one doesn't exist:

```
SECRET_KEY=changeme123
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/dbname
ALLOWED_HOSTS=127.0.0.1,localhost
```

pdate values before enabling production traffic.

### 🔐 Environment Configuration

- `DJANGO_SECRET_KEY`: Generate new secret key for the Django project.
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts.
- `DJANGO_DEBUG`: `True` or `False` (debug mode).
- `DATABASE_URL`: Full connection string for PostgreSQL.
- `CSRF_TRUSTED_ORIGINS`: Comma-separated list of trusted domains.
- `CONN_MAX_AGE`: DB connection max age in seconds (e.g. 60).

---


---

## 🔗 Usage

- Admin Panel: `/admin/`
- Home Page - Sign Up and Sign In buttons

---

## 🔒 Security & Configuration

- `SECURE_PROXY_SSL_HEADER`: Required if using SSL with Nginx
- Uses `django-allauth` for authentication using email address with verification

---

## 🧼 To Reset/Remove a Project

On the server run the following commands:

```bash
sudo systemctl stop gunicorn-myproject.socket
sudo systemctl disable gunicorn-myproject.socket
sudo rm /etc/systemd/system/gunicorn-myproject.*
sudo rm /etc/nginx/sites-available/myproject
sudo rm /etc/nginx/sites-enabled/myproject
sudo rm -rf /var/www/sites/myproject
sudo systemctl daemon-reload
sudo systemctl reload nginx
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
