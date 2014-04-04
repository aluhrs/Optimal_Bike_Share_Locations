import os

DB_URI = os.environ.get("DATABASE_URL", "sqlite:///bikeshare.db")
SECRET_KEY = os.environ.get("SECRET_KEY")
GOOGLE_API_KEY=os.environ.get("GOOGLE_API_KEY")