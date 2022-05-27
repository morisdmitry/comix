# creating database using docker-compose

after clone repo:

- prepare your environment
- pip install -r requirements.txt
- make your .env file. Just copy .env.file and remove the .file at the end
- start docker-compose file. for this you need installed docker
- upgrade db like: `flask db upgrade`
- run flask app

# creating database using docker-compose

`docker-compose up -d`

## go into database

`docker-compose exec postgres psql -U postgres -d comix_test`

# run flask app

`python wsgi.py`
