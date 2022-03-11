# Assessment for The Recycling Partnership

### Part 1

1a. Simple Flask app to POST, PUT, DELETE, and GET pets
1b. - In the templates, only the http verbs "POST" and "GET" are used. The HTML forms I have used do not allow other methods. As a result, I have taken "POST" and manipulated it as it were a "PUT" in `/edit` and "DELETE" in `/delete`. - I have included "PUT" and "DELETE" in the allowed methods since I use Postman for testing. It is possible to allow public traffic to this API. Though I wouldn't want public, unchecked traffic to delete records without thorough authorization

Note that if a POST is sent via postman, the "Body" must use `x-www-form-urlencoded`

Issue: When spinning down the container, the db's data all gets flushed away
Solution: tie the db to a volume instead of building it into the image

Issue: Error checking on my submit and edit endpoints leaves a lot to be desired
Solution: Organize a happy path that allows expansion on the model

Issue: The easiest way for me to show a user the available pets to search for was to just give a list of _all_ of them
Solution: - Pagination could be helpful here, only returning a list of 10-or-so. But the issue of the user not knowing the Pet's `id` immediately could be problematic - Could make `id` a unique and custom input from the user, like a password

Issue: This app has no security
Solutions: - Make secrets actually secret - Do not store `.env` in a repo - Include some API keys for the database

### Part 2a

1. To run this container, please pull the docker image:
2. `docker pull jake94a/trp-docker-flask:latest`
   1. https://hub.docker.com/repository/docker/jake94a/trp-docker-flask
3. Clone the repo (we need the `test.db`, `.env`, and startup script)
   1. In this case, unzip the folder into your desired directory
   2. Would typically put a GitHub URL here
4. Then run the image with the supplied `.env` and `test.db` files:
   1. From the `trp-docker-flask` directory
   2. `./bin/start.sh`
      - This script injects our environment variables
      - And mounts our database file as a volume

Issue: This script requires the developer to run the app in a too-specific way
Solution: running the database on a host port would be a more flexible solution

### Part 2b

The image has been tested with Snyk for vulnerabilities and was subsequently upgraded from `python:3.9.7` to `python:3.10.2-slim`

As far as endpoint testing goes:

- I am mostly familiar with Django's built-in testing libraries, plus some Node libraries, so I will move forward with that in mind
  - The Django-REST library I am most familiar with is built on `unittest`
- Create a couple example objects of things I would expect
  - Strings for Pet.name, Pet.species
  - Unique integer for Pet.id
- Assert that if a Pet.species that is not "dog" or "cat" returns an error
- Assert that valid requests return 200 status codes
- Assert that invalid requests return appropriate error messages
  - There are so many branches and tangents to take here
  - "Invalid species"
  - "Missing name/species/id"
  - "name is not a string"
  - "ID is not an integer"
  - verify "name" only allows valid characters
