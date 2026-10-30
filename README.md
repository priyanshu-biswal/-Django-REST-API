# Django REST API - Blog Posts

A Django REST Framework API for creating and managing blog posts. Users must
authenticate to access the API, and can only view or modify posts they created.

## Features

- Create, list, retrieve, update, and delete blog posts
- Django session and token authentication
- Per-user post visibility and ownership permissions
- Filter posts by creation date
- Search post titles and content
- Order results by post ID
- Paginated results with a fixed page size of five
- JSON API responses

## Project structure

```text
blog/
├── blog/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── helloworld/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── filters.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   └── views.py
├── manage.py
└── README.md
```

## Requirements

- Python 3.12 or later
- Django
- Django REST Framework
- django-filter

## Setup

Open a terminal in the directory containing `manage.py`, then create and
activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required packages and initialize the database:

```powershell
python -m pip install Django djangorestframework django-filter
python manage.py migrate
```

Optionally create an account for the Django admin:

```powershell
python manage.py createsuperuser
```

Start the development server:

```powershell
python manage.py runserver
```

The project is an API and does not provide a homepage at `/`. Use the API
endpoints below instead.

## Authentication

All post endpoints require authentication. To obtain a token, send a `POST`
request to `/api/token/` with JSON credentials:

```json
{
  "username": "your-username",
  "password": "your-password"
}
```

Include the returned token on subsequent API requests:

```http
Authorization: Token your-token
```

For session-based login, use `/api-auth/login/` in a browser or API client that
supports cookies and CSRF.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/token/` | Obtain an authentication token |
| `GET` | `/api/posts/` | List the signed-in user's posts |
| `POST` | `/api/posts/` | Create a post |
| `GET` | `/api/posts/{id}/` | Retrieve one of the user's posts |
| `PUT` / `PATCH` | `/api/posts/{id}/` | Update one of the user's posts |
| `DELETE` | `/api/posts/{id}/` | Delete one of the user's posts |

When creating a post, send `title` and `content` as JSON. The API sets the
author from the authenticated user; clients cannot assign a post to another
user.

## Filtering, search, ordering, and pagination

- Filter by creation date: `/api/posts/?created_at=2026-10-30`
- Search title and content: `/api/posts/?search=django`
- Order by ID ascending or descending: `/api/posts/?ordering=id` or
  `/api/posts/?ordering=-id`
- Select a page: `/api/posts/?page=2`

List responses use the standard paginated JSON shape with `count`, `next`,
`previous`, and `results`. Each page contains at most five posts.

## Tests

Run the API test suite from the directory containing `manage.py`:

```powershell
python manage.py test helloworld
```
