# Hosting the frontend

This directory contains all the code used to host a static website. The path of the static files must be either defined in the ```BUILD_PATH``` environment variable or by default they must be located in ```../client/dist```.

The hosting of these static items is performed via a simple Express server which can be reached from ```localhost:3000```.

# NOTE!

This server has cors set to ```*```.