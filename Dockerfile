# Use an official lightweight Python image.
FROM python:3.9-slim

# Install system dependencies required by WeasyPrint.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libgdk-pixbuf2.0-0 \
        libffi-dev \
        shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Continue with your existing Dockerfile setup...

# Set environment variables.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container.
WORKDIR /app

# Copy the dependencies file to the working directory.
COPY requirements.txt .

# Install any dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory.
COPY --chown=user:group app /app 

# Command to run the application.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]


