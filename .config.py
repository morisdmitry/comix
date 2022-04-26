
class Config:

    NAME_DB = 'dbname'
    USER = 'dbuser'
    PASSWORD = 'dbpassword'
    HOST = 'dbhost'
    PORT = '5432'

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}/{NAME_DB}'