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

# Expose Nuxt default port
EXPOSE 3000

# Start the app
CMD ["node", ".output/server/index.mjs"]
