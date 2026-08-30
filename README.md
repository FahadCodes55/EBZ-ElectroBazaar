# Electro Bazaar ⚡

Electro Bazaar is a specialized electronics e-commerce platform built using Python and Django. The system includes standard online retail functionality alongside deep product categorization, dynamic specifications handling, and secure Google OAuth integration.

---

## 🛠️ Tech Stack & Requirements

*   **Language:** Python 3.10+
*   **Framework:** Django 5.0+
*   **Environment:** Python `venv` (Virtual Environment)
*   **Authentication:** Django Auth + Google OAuth 2.0 (`django-allauth`)
*   **Database:** SQLite (Development) / PostgreSQL (Production)
*   **Media Handling:** Pillow (for product images)

---

## Set Up the Virtual Environment (venv)
# Create the environment
python -m venv venv

# Activate the environment (Windows)
venv\Scripts\activate

# Activate the environment (Mac/Linux)
source venv/bin/activate

## Install Dependencies
pip install -r requirements.txt

## Configure Environment Variables
DEBUG=True
SECRET_KEY=your_django_secret_key_here

GOOGLE_CLIENT_ID=your_google_client_id_here

GOOGLE_CLIENT_SECRET=your_google_client_secret_here

## Run Database Migrations & Start Server
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
