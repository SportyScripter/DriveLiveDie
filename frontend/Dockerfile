# Use an official Node.js runtime as the base image
FROM node:latest

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Start the Next.js development server
CMD ["npm", "run", "dev"]
