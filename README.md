# SheetShare

A web-based sheet music sharing forum built with Django. Users can upload, download, and discuss sheet music across a range of genres.

## Features

- User authentication (register, login, logout)
- Upload sheet music as PDF or image
- Browse and search posts by title, genre, or author
- Comment on posts
- User profiles with upload history
- Download tracking

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (development)
- **Frontend:** Bootstrap 5, custom CSS
- **Storage:** Local media files

## Setup
```bash
# Clone the repo
git clone git@github.com:Harry-GRO/sheetmusic.git
cd sheetmusic

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your SECRET_KEY

# Run migrations
python manage.py makemigrations forum accounts
python manage.py migrate

# Load genre seed data
python manage.py loaddata forum/fixtures/genres.json

# Create a superuser
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

## Environment Variables

Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Project Structure
```
sheetmusic/
├── forum/          # Posts, comments, genres
├── accounts/       # Auth, user profiles
├── templates/      # HTML templates
├── static/         # CSS
└── sheetmusic/     # Django config
```