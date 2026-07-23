# NotesHub Backend

Django REST API for the NotesHub note-taking application.

## Tech Stack

- Python / Django 6
- Django REST Framework
- SimpleJWT — authentication
- SQLite (dev) / PostgreSQL (prod)
- django-cors-headers
- django-filter

## Setup

```bash
# Clone and enter the project
git clone https://github.com/Joshua-dev559/NotesHub_backend.git
cd NotesHub_backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env   # then fill in values

# Run migrations
cd noteshub
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

## Environment Variables

Create a `.env` file inside `noteshub/`:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

## Project Structure

```
noteshub/
├── users/          # Auth, registration, user profile
├── notes/          # Notes CRUD and actions
├── categories/     # Note categories
├── search/         # Cross-model search
├── collaborations/ # Note sharing
├── notifications/  # User notifications
└── noteshub/       # Settings and root URLs
```

---

## API Documentation

Base URL: `http://localhost:8000/api`

All endpoints except `/register/`, `/token/`, and `/token/refresh/` require:
```
Authorization: Bearer <access_token>
```

---

### Authentication

#### Register
```
POST /api/register/
```
Body:
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "pass1234",
  "password2": "pass1234"
}
```
Response `201`:
```json
{
  "user": { "id": "uuid", "username": "john", "email": "john@example.com" },
  "access": "<token>",
  "refresh": "<token>"
}
```

---

#### Login
```
POST /api/token/
```
Body:
```json
{ "email": "john@example.com", "password": "pass1234" }
```
Response `200`:
```json
{ "access": "<token>", "refresh": "<token>" }
```

---

#### Refresh Token
```
POST /api/token/refresh/
```
Body:
```json
{ "refresh": "<refresh_token>" }
```
Response `200`:
```json
{ "access": "<new_access_token>" }
```

---

#### Get Current User
```
GET /api/me/
```
Response `200`:
```json
{
  "id": "uuid",
  "username": "john",
  "email": "john@example.com",
  "first_name": "",
  "last_name": "",
  "bio": "",
  "avatar_url": null,
  "notes_count": 3
}
```

---

#### Update Profile
```
PATCH /api/me/
```
Body (any subset):
```json
{ "first_name": "John", "bio": "Hello world" }
```

---

#### Logout
```
POST /api/logout/
```
Body:
```json
{ "refresh": "<refresh_token>" }
```
Response `205`

---

### Notes

#### List Notes
```
GET /api/notes/
```
Query params:
| Param | Example | Description |
|-------|---------|-------------|
| `search` | `?search=meeting` | Search title, content, tags |
| `is_pinned` | `?is_pinned=true` | Filter pinned notes |
| `is_archived` | `?is_archived=false` | Filter archived notes |
| `category` | `?category=<uuid>` | Filter by category |
| `ordering` | `?ordering=-updated_at` | Sort field |

Response `200`:
```json
{
  "count": 2,
  "results": [
    {
      "id": "uuid",
      "title": "My Note",
      "content": "<p>Hello</p>",
      "category": { "id": "uuid", "name": "Work", "color": "#cbf0f8" },
      "is_pinned": false,
      "is_archived": false,
      "color": "#ffffff",
      "tags": ["work", "ideas"],
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

#### Create Note
```
POST /api/notes/
```
Body:
```json
{
  "title": "My Note",
  "content": "<p>Hello world</p>",
  "color": "#ffffff",
  "tags": ["work"],
  "category_id": "uuid"
}
```
Response `201`: note object

---

#### Get Note
```
GET /api/notes/<id>/
```

#### Update Note
```
PUT /api/notes/<id>/
```

#### Partial Update
```
PATCH /api/notes/<id>/
```

#### Delete Note
```
DELETE /api/notes/<id>/
```
Response `204`

---

#### Toggle Pin
```
POST /api/notes/<id>/toggle_pin/
```
Response `200`: full note object with updated `is_pinned`

---

#### Toggle Archive
```
POST /api/notes/<id>/archive/
```
Response `200`: full note object with updated `is_archived`

---

### Categories

#### List Categories
```
GET /api/categories/
```

#### Create Category
```
POST /api/categories/
```
Body:
```json
{ "name": "Work", "color": "#cbf0f8" }
```

#### Update Category
```
PUT /api/categories/<id>/
```

#### Delete Category
```
DELETE /api/categories/<id>/
```

---

### Search

#### Search Notes
```
GET /api/search/?q=<query>
```
Response `200`:
```json
{
  "notes": [ ...note objects ]
}
```

---

### Collaborations

#### List Collaborations
```
GET /api/collaborations/
```

#### Add Collaborator
```
POST /api/collaborations/
```
Body:
```json
{
  "note": "<note_uuid>",
  "user": "<user_uuid>",
  "role": "viewer"
}
```
Roles: `viewer`, `editor`

#### Update Role
```
PATCH /api/collaborations/<id>/
```
Body:
```json
{ "role": "editor" }
```

#### Remove Collaborator
```
DELETE /api/collaborations/<id>/
```

---

### Notifications

#### List Notifications
```
GET /api/notifications/
```

#### Mark One as Read
```
POST /api/notifications/<id>/mark_read/
```

#### Mark All as Read
```
POST /api/notifications/mark_all_read/
```

---

## Running Tests

```bash
python manage.py test
```

## Branch Strategy

```
feature/* → develop → main
```
- All features are developed on `feature/` branches
- PRs are merged into `develop` after review
- `develop` is merged into `main` after testing
