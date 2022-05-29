import os


class Config:
    IMG_DIR = os.environ.get("IMG_DIR")
    NAME_DB = os.environ.get("DB_NAME")
    USER = os.environ.get("DB_USER")
    PASSWORD = os.environ.get("PASSWORD")
    HOST = os.environ.get("HOST")
    PORT = os.environ.get("PORT")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME_DB}"
