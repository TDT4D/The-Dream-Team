# The frontend service

This directory contains everything for the frontend service. The frontend client application uses React functional components and is written in TS. This app is then turned built and hosted staticly via Express. The code used to generate the client is found under [/client](./client/) and the server used to host the static build is under [/server](./server/). To produce a proper service, these then combined within the [Dockerfile](./Dockerfile).

# Usage

To build the application you can simply use Docker build. It is possible to supply to following build arguments:
- DEMO_MODE
    - Type = boolean
    - Default = false
    - If DEMO_MODE == true, all the Student's names will set to fake names
- ML_TYPE=advanced
    - Type = advanced | basic
    - Default = advanced
    - Defines which type of machine learning model we will be using. If anyother model than the randomforest (the most basic one), use advanced.

After building the image, the container can be run using Docker run. **Note!** No be able interact with the application, the container's port 3000 needs to be exposed.

## Example commands

Building the container
```shell
docker build -t frontend:latest .
```

Running the container and exposing the port 3000
```shell
docker run -p "3000:3000" frontend
```

Now the application should be avaible at ```localhost:3000```.