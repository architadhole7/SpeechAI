# Use a lightweight Python image
FROM python:3.10-slim

# Install Java (required for language-tool-python)
RUN apt-get update && apt-get install -y default-jre && apt-get clean

# Create working directory
WORKDIR /app

# Install Python dependencies first (faster builds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose port for Flask
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
