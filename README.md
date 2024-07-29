# Python Web application for XML conversion

## Background

Hey guys, I'm a C# backend engineer with no commercial Python experience and I haven't seen Python in years. However, I've decided to take on the challenge of building this assignment solution as best as I possibly can. Despite Python not being my main language, I'm strong in software engineering principles and am not afraid to take on new challenges, but there are some... cultural differences, when it comes to coding in C# and Python.

With a lot of googling, time spent on StackOverflow and some IDE specific tools, I managed to come up with the solution.

Some parts of the code contain comments about how I'd approach specific issues, they're mostly talking points.

Hope it's not too far off and we can talk about this in another session. 😄

## Environment Variables

The following environment variables are used in this application:

- `EXPORT_USERNAME`: Specifies the username for authorization when using the API.
- `EXPORT_PASSWORD`: Specifies the password for authorization when using the API.
- `ROSSUM_API_BASE_URL`: Specifies the base URL for the Rossum API.
- `ROSSUM_API_USERNAME`: Specifies the username for authentication with the Rossum API.
- `ROSSUM_API_PASSWORD`: Specifies the password for authentication with the Rossum API.
- `POSTBIN_API_BASE_URL`: Specifies the base URL for the Postbin API.

Make sure to set these environment variables with the appropriate values before running the application.


## Running the Solution

To run the solution, follow these steps:

1. Fill in the necessary variables in the `.env` file.
2. Run `docker-compose build` to build the Docker containers.
3. Run `docker-compose up` to start the web API.

That's it! The solution should now be up and running.


## Using the API

To use the API, send a POST request to the following endpoint:

```
http://127.0.0.1:5000/export
```

The request should be authorized using username and password. Include the following JSON payload in the request body:

```json
{
    "annotation_id" : "<annotation_id>",
    "queue_id" : "<queue_id>"
}
```

Here's an example curl script to make the request:

```bash
curl -X POST -u username:password -H "Content-Type: application/json" -d '{
    "annotation_id" : "3425119",
    "queue_id" : "1196410"
}' http://127.0.0.1:5000/export
```

Make sure to replace `username` and `password` with your actual credentials, and `<your_annotation_id>` and `<your_queue_id>` with the appropriate values.

That's all you need to do to use the API!
