# Stage 1: Build the app
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

# Copy the full app source
COPY . .

# Build the Nuxt app
RUN yarn build

# Stage 2: Run the app with minimal image
FROM node:20-alpine AS runner

WORKDIR /app

# Install only production dependencies
COPY package.json yarn.lock ./
RUN yarn install --production --frozen-lockfile

# Copy the built app from builder stage
COPY --from=builder /app/.output ./.output

ARG RAILWAY_PUBLIC_DOMAIN
ARG RAILWAY_PRIVATE_DOMAIN
ARG RAILWAY_PROJECT_NAME
ARG RAILWAY_ENVIRONMENT_NAME
ARG RAILWAY_SERVICE_NAME
ARG RAILWAY_PROJECT_ID
ARG RAILWAY_ENVIRONMENT_ID
ARG RAILWAY_SERVICE_ID
ARG BASE_URL

ENV BASE_URL=$BASE_URL \
  RAILWAY_PUBLIC_DOMAIN=$RAILWAY_PUBLIC_DOMAIN \
  RAILWAY_PRIVATE_DOMAIN=$RAILWAY_PRIVATE_DOMAIN \
  RAILWAY_PROJECT_NAME=$RAILWAY_PROJECT_NAME \
  RAILWAY_ENVIRONMENT_NAME=$RAILWAY_ENVIRONMENT_NAME \
  RAILWAY_SERVICE_NAME=$RAILWAY_SERVICE_NAME \
  RAILWAY_PROJECT_ID=$RAILWAY_PROJECT_ID \
  RAILWAY_ENVIRONMENT_ID=$RAILWAY_ENVIRONMENT_ID \
  RAILWAY_SERVICE_ID=$RAILWAY_SERVICE_ID

# Expose Nuxt default port
EXPOSE 3000

# Start the app
CMD ["node", ".output/server/index.mjs"]
