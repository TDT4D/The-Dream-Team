# Contents

This directory contains all the different services (aka. non UI related components).


## API

All the functionality for handling API calls to the backend.

## ML

All functions for setting and getting the machine learning models' status and the set teamsize from [storage](./storage/storage.service.ts).

## Project

Contains all the functionality to get the projects from the backend or a predifined set of dummy projects if running as a standalone.

## Score

Contains all the functionality to get the applicant scores from the backend or a predifined scores.

## Storage

Utility functions used to store objects into persistant storage. In the case of this app we simply use the browser localstorage, but this could be easily swapped out for some other solution.

## Student

All the functionality to set and get the student's labels or location into persistant storage. Also contains the function to retrieve all the student's for a given project or a predifined set of dummy students if running as a standalone.