# Car Dealership

A vehicle-listing web application built with Django and HTMX. Visitors can browse, search and filter cars, with page content updating without full-page reloads.

**Live demo:** https://car-dealership-vtxu.onrender.com
**Code:** https://github.com/asb01-er/Car_Dealership

> The demo runs on a free Render server, so the first load can take up to 30 seconds.

## Features

- Browse available vehicles
- Search and filter listings
- HTMX-driven requests that update the page without a full reload
- Server-rendered Django templates

## Tech stack

- Python
- Django
- HTMX
- HTML and CSS

## Getting started

### Prerequisites

- Python 3.10+

### Setup

```bash
git clone https://github.com/asb01-er/Car_Dealership.git
cd Car_Dealership

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000.

To manage listings from the admin site, create a superuser:

```bash
python manage.py createsuperuser
```

Then visit `/admin`.

## Deployment

Deployed on Render as a Python web service. Set `SECRET_KEY` and other environment variables in Render, run `python manage.py collectstatic` during the build, and start the app with Gunicorn.

## Author

**Ernest Ekelem** — [GitHub](https://github.com/asb01-er) · [LinkedIn](https://www.linkedin.com/in/ernest-ekelem-5a771735a)
