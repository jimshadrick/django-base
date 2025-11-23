# Django Base Project Template (Bootstrap)

A sample base template that can be used for a new Django project, with support for local development and VPS-based
production deployment.

---

## Project Structure

- `project/`: Contains the main Django project configuration.
- `core/`: Contains the core application models and logic.
- `users/`: App for user account management and password changes.
- `manage.py`: Django management script for running commands.
- `init_env.sh`: One-time script to scaffold the .env file and prepare the project directory.
- `setup_deploy.sh`: Reproducible deployment script for DigitalOcean VPS.
- `post_deploy.sh`: Post-deployment script to apply migrations, collect static files, etc.

---

## Local Development Setup

1. Clone the repository.
2. Install the necessary dependencies using `uv sync`
3. Create the database `djbasedb` on your PostgreSQL server.
3. Create and update your `.env.dev` file with the correct database credentials (example below):
    ```env
    DJANGO_DEBUG=True
    DJANGO_SECRET_KEY=supersecretkey
    DATABASE_URL=postgres://postgres:postgres@db:5432/djbasedb
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
    CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
    CONN_MAX_AGE=60
    EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend OR leave blank (Django console.EmailBackend)
    MAILGUN_API_KEY=changeme
    MAILGUN_DOMAIN=sandboxid.mailgun.org
    DEFAULT_FROM_EMAIL=admin@localhost
    SITE_DOMAIN=mydomain.com
    SITE_NAME=mydomain
    ```
4. Run migrations and setup: `./post_deploy.sh`
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

## Package Dependencies
uv pkg manager:
- `python = >=3.13`
- `django>=5.1.7`
- `environs[django]>=14.1.1`
- `gunicorn>=23.0.0`
- `psycopg[binary]>=3.2.6`
- `whitenoise>=6.9.0`
- `django-allauth[socialaccount]>=65.7.0`
- `django-anymail[mailgun]>=13.0`
- `django-debug-toolbar>=5.1.0`

CDN:
- `bootstrap.min.css=5.3.5`  
- `bootstrap-bundle.min.js=5.3.5`

Minified files (for development only)
- `/static/css/vendor/bootstrap.min.css`
- `/static/css/vendor/bootstrap-bundle.min.js`

---

## Environment Configuration

- `DJANGO_SECRET_KEY`: Secret key for the Django project.
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts.
- `DJANGO_DEBUG`: `True` or `False` (debug mode).
- `DATABASE_URL`: Full connection string for PostgreSQL.
- `CSRF_TRUSTED_ORIGINS`: Comma-separated list of trusted domains.
- `CONN_MAX_AGE`: DB connection max age in seconds (e.g. 60).
- `EMAIL_BACKEND`: Specify either the `anymail.backends.mailgun.EmailBackend` for prod or leave blank
- `MAILGUN_API_KEY`: API key for Mailgun.
- `MAILGUN_DOMAIN`: Domain for Mailgun.
- `DEFAULT_FROM_EMAIL`: Default email address.
- `SITE_DOMAIN`: Domain for the site.
- `SITE_NAME`: Name for the site.

---

## Production Deployment (DigitalOcean VPS)

This app contains scripts to deploy the project to a VPS manually using Bash scripts. This allows you to manage
deployments without requiring CI/CD.

### Prerequisites for Production

- VPS provisioned (e.g., DigitalOcean droplet or another VPS provider)
- Non-root user (e.g., `myuser`) configured with sudo access
- SSH access to the VPS
- VPS updated and system packages installed (
  `nginx postgresql postgresql-contrib python3-dev libpq-dev curl build-essential`)
- Python 3.13+ and `uv` installed
- PostgreSQL running and accessible
- Postgres database created (`djbasedb`) and `djdbuser` created and assigned permissions to database and public schema
- DNS and domain setup (optional)

---

### Scripts for VPS Deployment (Located in project root)

| Script             | Purpose                                                                                                                                                                                                                             |
|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `init_env.sh`      | One-time script to create `/var/www/sites/<project>` and scaffold a placeholder `.env` file. Must be run AFTER first deployment using `sudo`.                                                                                       |
| `setup_deploy.sh`  | Main deployment script. Wipes project directory, clones repo, restores `.env`, installs dependencies, and optionally runs `post_deploy.sh`. Must be run under `myuser` account. The first time it is run use th `--skip-post` flag. |
| `post_deploy.sh`   | Invoked by `setup_deploy.sh`. Runs Django commands: `migrate`, `collectstatic`, and `init_site`. Must be run under `myuser` account.                                                                                                |
| `setup_configs.sh` | One-time script to generate and install and configure the Gunicorn and Nginx socket and service files. Must be run under `sudo`.                                                                                                    |
| `setup_ssl.sh`     | One time script, used to install and configure a self-signed SSL certificate using Certbot. Must be run under `sudo`. Pre-requisites: domain must be registered and email must be provided.                                         |

### Deployment steps:

1. SSH into your server `ssh myuser@your-server-ip` using the non-root user `myuser` created above.
2. Copy the `init_env.sh`, `setup_deploy.sh` and `setup_configs.sh` scripts to `/opt/scripts`.

#### _Initial Deployment Only_

3. Run the `setup_configs.sh` script to generate and deploys Gunicorn and Nginx configs for the application.

```bash
sudo ./setup_configs.sh <project_name> <deploy_user>
```

4. Edit the `.env_prod` file created, replace with real values, and copy the file to the APP_DIR before running the
   deployment script.

```bash
cp /opt/scripts/.env.prod /var/www/sites/myproject/
```

#### _Future Deployments (pull latest changes and redeploy)_

5. Run the `setup_deploy`

```bash
./setup_deploy.sh <project_name>
```

By default, `setup_deploy.sh` calls `post_deploy.sh` to run post deployment tasks (migrations, static files, etc.)

## Usage

- Admin Panel: `/admin/`
- Home Page - Sign Up and Sign In buttons

---

## Security & Configuration

- `SECURE_PROXY_SSL_HEADER`: Required if using SSL with Nginx
- Uses `django-allauth` for authentication using email address with verification

---

## To Uninstall/Remove a Project

On the server run the following scripts (under `sudo`:

| Script              | Purpose                                                                                                                                               |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| `uninstall_app.sh`  | One-time script to remove the project directory and related application code as well as related Nginx and Gunicorn socket and service files and logs. |
| `uninstall_db.sh`   | One-time script to remove the project database and user and clean up connections.                                                                     |
| `uninstall_cert.sh` | One-time script to remove the Cloudflare origin certificate files (optional).                                                                         |

---

## Template Change Log

0.1.0 - Initial template structure
0.2.0 - Add deployment scripts
0.3.0 - Improve authentication setup and formatted templates
0.4.0 - Add email configuration with AnyMail and Mailgun
0.5.0 - Polish deployment process
0.5.1 - Fixed hardcoded ref in scripts, added env variable validation and comments

### v0.5.1 (Current Template Version)

- ✅ Django 5.1.7 with modern configuration
- ✅ User authentication and customized email templates using django-allauth
- ✅ VPS deployment scripts tested
- ✅ PostgreSQL integration working
- 🚧 SSL setup needs more testing
- 🚧 Email configuration could be simplified

### Template Roadmap

- [ ] Automatic logout for signed-in users after specified period
- [ ] Implement time zones tracking for users
- [ ] Add automated testing setup

---

## License

This project is licensed under the [MIT License](LICENSE).
