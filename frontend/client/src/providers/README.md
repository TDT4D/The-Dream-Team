# Contents

This directory contains all the different global context providers for the application and a helper function in [providers.tsx](./providers.tsx) to nest multiple providers within eachother.

## Auth

Provides a context used in setting, storing and providing the user's authentication token.

## ML

Provides a context used in setting and providing the status of the machine learning model and the user's set team size.

## Project

Provides a simple context used to passing around data about the user's currently selected project.

## Router

Provides the browser router and defines all the routes for the application.