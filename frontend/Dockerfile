# =================================================
#              Create a static SPA app
# =================================================
FROM node:23-alpine AS build

WORKDIR /app

# Create environment
COPY client/package*.json ./
RUN npm install

# Copy other files
COPY client .

# Environment variable for demo mode
ARG DEMO_MODE
ENV VITE_DEMO_MODE=${DEMO_MODE:-false}

# Set API endpoint env variable
ENV VITE_API_ENDPOINT=http://localhost/api

# Build the static SPA app
RUN npm run build

# =================================================
#                   Host the app
# =================================================
FROM node:23-alpine

WORKDIR /express-app

# Get the static files
RUN mkdir client
COPY --from=build /app/dist client/build/

# Create server environment
COPY server/package*.json .
RUN npm install

# Copy server files
COPY server .

# Set build path & start the application on port 3000
ENV BUILD_PATH=./client/build
CMD ["npm", "start"]
EXPOSE 3000
