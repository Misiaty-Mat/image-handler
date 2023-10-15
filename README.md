# Image handler Django Rest Framework application
## Setup
`docker-compose build `

## Run application
`docker-compose up`

## Features and endpoints
- `GET http://localhost:8000/api/userimage/userimage/` - list image links
- `POST http://localhost:8000/api/userimage/userimage/` - create new image
- `GET http://localhost:8000/api/userimage/userimage/{:id}/` - image details
- `PUT http://localhost:8000/api/userimage/userimage/{:id}/` - edit image details
- `DELETE http://localhost:8000/api/userimage/userimage/{:id}/` - delete image
- `GET http://localhost:8000/api/userimage/userimage/{:id}/thumbnail/?image_height=200` - get image thumbnail with height of 200
- `GET http://localhost:8000/api/userimage/userimage/{:id}/thumbnail/?image_height=400` - get image thumbnail with height of 400
- `GET http://localhost:8000/api/userimage/userimage/{:id}/generate-link/?live_time={:time_in_seconds}` - get a link for temporary access to an image for given number of seconds
- `GET http://localhost:8000/admin` - go to admin page

## Important information
- Remember to create `.env` file in the `/app/app` directory. Right where the `.env.sample` file is and set `SECRET_KEY` value
- System does not support registration
- To create admin user run: `docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py createsuperuser"`
- To login go to admin page
- System automaticly supply database with 3 default account tiers: 'Basic', 'Premium', 'Enterprice'
- To test the application run: `docker-compose run --rm app sh -c "python manage.py test"`
- To check lint of application code run: `docker-compose run --rm app sh -c "flake8"`