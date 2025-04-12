# Django Base Project Example

A sample base template that can be used for a new Django project.

## Project Structure

- `project`: Contains the main Django project configuration.
- `core`: Contains the core application models and logic.
- `accounts`: App for user account management and password changes.
- `manage.py`: Django management script for running commands.

## Setup Instructions

1. Clone the repository.
2. Install the necessary dependencies using `uv sync`
3. Change the `DATABASE_URL` environment variable in `.env` to match your Postgres configuration
    - Create the database in the Postgres container and update the hostname and db name accordingly
    - Example: `DATABASE_URL=postgres://postgres:postgres@localhost:5432/djbasedb`
4. Run `uv run manage.py migrate` to apply migrations
5. Run `uv run manage.py collectstatic` to collect static files
6. Run `uv run manage.py createsuperuser` to create a superuser
7. Start the Django development server using `uv run manage.py runserver`
8. Connect to the web app at `http://localhost:8000/admin`

### Package Dependencies

- django>=5.1.7
- environs[django]>=14.1.1
- gunicorn>=23.0.0
- psycopg[binary]>=3.2.6
- whitenoise>=6.9.0
- django-allauth[socialaccount]>=65.7.0

### Environment Variables

- `DJANGO_SECRET_KEY`: Secret key for the Django project.
- `DJANGO_ALLOWED_HOSTS`: List of allowed hosts for the Django project.
- `DJANGO_DEBUG`: Boolean value indicating whether the Django project is in debug mode.
- `DATABASE_URL`: Database connection string for the Django project.
- `CSRF_TRUSTED_ORIGINS`: List of trusted origins for the Django project.
- `CONN_MAX_AGE=60`: Maximum connection age in seconds for the database.

##### Example `.env` file

DJANGO_DEBUG=True
DJANGO_SECRET_KEY=supersecretkey
DATABASE_URL=postgres://postgres:postgres@db:5432/djbasedb
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
CONN_MAX_AGE=60

### Additional Configuration

- `SECURE_PROXY_SSL_HEADER`: Header used to detect secure requests coming from behind a proxy.
- `AUTH_USER_MODEL`: Custom user model for the Django project.

## Usage

- Access the admin panel at `/admin/`.
- View the home page placeholder at `/`.

## Additional Information

- The project uses a local PostgreSQL database by default.
- The project uses `django-allauth` for user authentication and templates are styled using Bootstrap 5.

## License

This project is licensed under the [MIT License](LICENSE).