import os

# put the db url in here
DB_URI = os.environ.get("DATABASE_URL", "sqlite:///bikeshare.db")
SECRET_KEY = os.environ.get("SECRET_KEY")