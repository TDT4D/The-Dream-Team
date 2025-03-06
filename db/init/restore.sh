#!/bin/bash

# Restore from dump
mongorestore --archive=./docker-entrypoint-initdb.d/mongo.gz --gzip
