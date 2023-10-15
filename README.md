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