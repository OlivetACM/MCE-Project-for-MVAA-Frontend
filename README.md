# MCE-Project-for-MVAA-Frontend
Frontend website for the Military Credit Equivalency project


### Run this server by following these steps:
  1. Navigate to the `www` directory
  2. Run `python3 manage.py migrate`
  3. Run `python3 manage.py runserver`
  4. Open a browser and then go to `127.0.0.1:8000`
  
### To run within docker:
  1. To build the container run `sudo docker-compose build`
  **This only needs to be ran when you change `requirements.txt`, `compose/webserver/Dockerfile`, or `docker-compose.yml`
  2. To run the Django server run `docker-compose up`

### To access the command line within docker:
  1. docker ps -a //This lists the container processes. You'll need the container ID for our container.
  2. docker exec -it <container id> /bin/bash //This is effectively a chroot (change root) operation.
