FROM python:3.10-slim

# Install Java for language-tool-python
RUN apt-get update && \
    apt-get install -y openjdk-17-jre && \
    apt-get clean

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole project
COPY . .

# Expose port
EXPOSE 5000

# Start the app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "api.app:app"]
