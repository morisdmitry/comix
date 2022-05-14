  

# creating database using docker-compose

`docker-compose build --no-cache`
`docker-compose up -d`

## go into database

`docker-compose exec postgres psql -U postgres -d comix_test`

# run flask app

`python wsgi.py`