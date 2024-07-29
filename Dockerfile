# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install dependencies and Google Chrome
RUN apt-get update \
    && apt-get install -y wget gnupg \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get install -y libxpm4 libxrender1 libgtk2.0-0 libnss3 libgconf-2-4 \
    && rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Install Python dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the project files
COPY ./zospital-Api /app

# Copy credentials.json
COPY ./credentials.json /app/credentials.json

# Copy entrypoint script and ensure it has execution permissions
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PORT 8000
# Expose the port
EXPOSE 8000

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]