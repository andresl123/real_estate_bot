# # Use an official Python runtime as a parent image
# FROM python:3.9-slim

# # Install necessary packages
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     locales \
#     && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
#     && locale-gen \
#     && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Set environment variables for Python to use this locale
# ENV LANG=en_US.UTF-8
# ENV LC_ALL=en_US.UTF-8

# # Set the working directory in the container
# WORKDIR /app

# # Copy only requirements first to leverage Docker cache
# COPY requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the current directory contents into the container
# COPY . /app

# # Expose the port the app runs on
# EXPOSE 5000

# # Run the application
# CMD ["python", "main.py"]
# #CMD ["locale"]

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install necessary packages, including SQLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    sqlite3 \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Python to use this locale
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . /app

# Run the application
CMD ["python", "main.py"]
