# Django Base Project Example

A sample base template that can be used for a new Django project, with support for local development and VPS-based
production deployment.

---

## 🗂 Project Structure

- `project/`: Contains the main Django project configuration.
- `core/`: Contains the core application models and logic.
- `accounts/`: App for user account management and password changes.
- `manage.py`: Django management script for running commands.
- `init_env.sh`: One-time script to scaffold the .env file and prepare the project directory.
- `setup_deploy.sh`: Reproducible deployment script for DigitalOcean VPS.
- `post_deploy.sh`: Run after deploy to apply migrations, collect static files, etc.

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

This app contains scripts to deploy the project to a VPS manually using Bash scripts. This allows you to manage
deployments without requiring CI/CD.

### 🔧 Prerequisites

- VPS provisioned (e.g., DigitalOcean droplet)
- Non-root user (e.g., `myuser`) configured with sudo access
- SSH access to the VPS
- VPS updated and system packages installed (
  `nginx postgresql postgresql-contrib python3-dev libpq-dev curl build-essential`)
- Python 3.13+ and `uv` installed
- PostgreSQL running and accessible
- Postgres database created (`djbasedb`) and `djdbuser` created and assigned permissions to database and public schema
- DNS and domain setup (optional)

---

### 📂 Scripts for VPS Deployment (Located in project root)

| Script             | Purpose                                                                                                                                                                                                                             |
|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `init_env.sh`      | One-time script to create `/var/www/sites/<project>` and scaffold a placeholder `.env` file. Must be run AFTER first deployment using `sudo`.                                                                                       |
| `setup_deploy.sh`  | Main deployment script. Wipes project directory, clones repo, restores `.env`, installs dependencies, and optionally runs `post_deploy.sh`. Must be run under `myuser` account. The first time it is run use th `--skip-post` flag. |
| `post_deploy.sh`   | Invoked by `setup_deploy.sh`. Runs Django commands: `migrate`, `collectstatic`, and `init_site`. Must be run under `myuser` account.                                                                                                |
| `setup_configs.sh` | One-time script to generate and install and configure the Gunicorn and Nginx socket and service files. Must be run under `sudo`.                                                                                                    |
| `setup_ssl.sh`     | One time script, used to install and configure a self-signed SSL certificate using Certbot. Must be run under `sudo`. Pre-requisites: domain must be registered and email must be provided.                                         |

---

### 🧪 First-Time Deployment (per app)

```bash
# SSH into your server
ssh myuser@your-server-ip

# Create the scripts directory if it doesn't exist
sudo mkdir -p /opt/scripts
sudo chown $USER:www-data /opt/scripts  # optional: let your user manage it

# On your local machine - copy the following scripts to the server
scp init_env.sh myuser@your-server:/opt/scripts/init_env.sh
scp init_env.sh myuser@your-server:/opt/scripts/setup_deploy.sh

# Make the scripts executable
sudo chmod +x /opt/scripts/init_env.sh
sudo chmod +x /opt/scripts/setup_deploy.sh

# Run the deployment script as the NON-ROOT user with the optional `--skip-post` flag
/opt/scripts/setup_deploy.sh myproject myuser --skip-post

# Run one-time initialization
sudo /opt/scripts/init_env.sh myproject myuser

# Edit the generated .env with real values
sudo nano /var/www/sites/myproject/.env

# Activate the virtual environment
cd /var/www/sites/myproject
source venv/bin/activate  

# Run the post-deployment script as the NON-ROOT user
./post_deploy.sh

# Perform a quick test of the deployment using the Django development server (optional)
Do not use runserver for production. This is only a brief sanity check
    - Temporarily allow port 8000 in DO Cloud Firewall as and Inbound rule.
    - Run: uv run python manage.py runserver 0.0.0.0:8000`.
    - Access: http://YOUR_DROPLET_IP:8000.
    - If it works, stop the server (Ctrl+C).
    - **Crucially: Remove the temporary port 8000 rule from your DO Cloud Firewall.**

# Setup Gunicorn and Nginx configs 
sudo ./setup_configs.sh myproject myuser

# Perform a quick test of the deployment using Gunicorn
- Temporarily allow port 8000 in DO Cloud Firewall as and Inbound rule.
- Run: uv run gunicorn myproject.wsgi:application --bind 0.0.0.0:8000`.
- Access: http://YOUR_DROPLET_IP:8001.

# Check the status of the socket and service
sudo systemctl status gunicorn-myproject.socket
sudo systemctl status gunicorn-myproject.service

# Restart Gunicorn manually if needed
sudo systemctl restart gunicorn-myproject

# Test that the socket is working and Nginx is reverse proxying
curl -I http://localhost
- Verify you are getting `HTTP/1.1 200 OK`.
```

---

### 🔁 Future Deployments (pull latest changes and redeploy)

```bash
./setup_deploy.sh myproject
```

By default, `setup_deploy.sh` calls `post_deploy.sh`, which executes:

```bash
uv run python manage.py migrate --noinput
mkdir -p staticfiles
uv run python manage.py collectstatic --noinput
uv run python manage.py init_site
```

---

### 🔐 .env Creation Logic

The `init_env.sh` script will generate a default `.env` file like this if none exists:

```
SECRET_KEY=changeme123
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/dbname
ALLOWED_HOSTS=127.0.0.1,localhost
```

Update values before running the `post_deploy.sh` script and before enabling production traffic.

---

### Installing and Configuring SSL

Before enabling production traffic, setup and secure your domain with a self-signed SSL certificate.

1. **Register a Domain**
    - Use a provider like Namecheap, GoDaddy, Google Domains, etc.


2. **Set DNS A Record**
    - Go to your domain registrar’s DNS settings
    - Create an A record:
        - **Host**: `@`
        - **Points to**: your Droplet's IP address
        - **TTL**: default (e.g., 3600 seconds)


3. **Optional:** Add a second A record:
    - **Host**: `www`
    - **Points to**: your Droplet's IP


4. **Wait for DNS Propagation**
    - Can take up to a few minutes to an hour
    - Use tools like https://dnschecker.org to confirm your domain resolves to your Droplet


5. **Update Nginx config (Optional)**
    - Ensure your `server_name` line matches the domain(s):
      ```nginx
      server_name your_domain.com www.your_domain.com;
      ```

6. **Run the script to configure SSL**
   ```bash
   sudo ./setup_ssl.sh myproject your_domain.com your@email.com
   ```

7. **Verify Firewall Configuration**
    - Ensure HTTPS (TCP port 443) is allowed in your DigitalOcean Cloud Firewall.


8. **Test HTTPS Access**
    - **Visit `https://your_domain.com`. You should see a lock icon and your site should load securely.

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
